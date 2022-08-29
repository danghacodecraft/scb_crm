from pydantic import ValidationError

from app.api.base.controller import BaseController
from app.api.v1.endpoints.file.repository import repos_download_file
from app.api.v1.endpoints.tablet.mobile.repository import (
    repos_init_booking_authentication,
    repos_update_current_booking_authentication_by_tablet_id
)
from app.api.v1.endpoints.tablet.web.repository import (
    repos_create_tablet_otp, repos_delete_tablet_if_exists,
    repos_get_customer_avatar_url_and_full_name_if_exist_by_booking_authentication_id,
    repos_retrieve_and_init_if_not_found_booking_authentication,
    repos_retrieve_tablet
)
from app.api.v1.endpoints.tablet.web.schema import (
    TabletActionProcessingTransactionExtraData, TabletActionSignExtraData,
    TabletSwitchScreenRequest
)
from app.api.v1.endpoints.user.repository import repos_get_username_from_token
from app.api.v1.others.booking.repository import repos_check_exist_booking
from app.settings.event import INIT_SERVICE, service_rabbitmq
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, MOBILE_ACTION_NEW_TRANSACTION,
    MOBILE_ACTION_PROCESS_TRANSACTION, MOBILE_ACTION_SIGN,
    MOBILE_ACTION_TAKE_DOCUMENT_PHOTO, MOBILE_ACTION_TAKE_FACE_PHOTO,
    MOBILE_ACTION_UNPAIRED
)
from app.utils.error_messages import (
    ERROR_BOOKING_ID_NOT_EXIST, ERROR_TABLET_IS_NOT_PAIRED
)
from app.utils.tablet_functions import (
    get_client_broker_config_info, get_topic_name
)


class CtrTabletWeb(BaseController):
    async def ctr_get_otp_and_mqtt_info(self):
        old_tablet_info = self.call_repos(
            await repos_retrieve_tablet(
                teller_username=self.current_user.user_info.username,
                session=self.oracle_session
            )
        )
        if old_tablet_info['tablet_id']:
            # gửi cho mobile (tablet đã kết nối trước đó) message thông báo unpaired
            service_rabbitmq.publish(
                message={
                    "action": MOBILE_ACTION_UNPAIRED,
                    "data": {}
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_MOBILE,
                    tablet_id=old_tablet_info['tablet_id'],
                    otp=old_tablet_info['otp']
                )
            )

        otp_info = self.call_repos(
            await repos_create_tablet_otp(
                teller_username=self.current_user.user_info.username,
                session=self.oracle_session
            )
        )

        web_stomp_info = get_client_broker_config_info(device_type=DEVICE_TYPE_WEB)
        web_stomp_info['topic_name'] = get_topic_name(
            device_type=DEVICE_TYPE_WEB,
            tablet_id=otp_info['tablet_id'],
            otp=otp_info['otp']
        )

        return self.response({
            'otp_info': otp_info,
            'web_stomp_info': web_stomp_info
        })

    async def ctr_unpair_tablet(self, token: str):
        teller_username = self.call_repos(
            await repos_get_username_from_token(
                token=token
            )
        )

        tablet_info = self.call_repos(
            await repos_retrieve_tablet(
                teller_username=teller_username,
                session=self.oracle_session
            )
        )

        if tablet_info['tablet_id']:
            # gửi cho mobile message thông báo unpaired
            service_rabbitmq.publish(
                message={
                    "action": MOBILE_ACTION_UNPAIRED,
                    "data": {}
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_MOBILE,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )

        self.call_repos(
            await repos_delete_tablet_if_exists(
                teller_username=teller_username,
                session=self.oracle_session
            )
        )

        return self.response(None)

    async def ctr_switch_tablet_screen(self, request: TabletSwitchScreenRequest):
        tablet_info = self.call_repos(
            await repos_retrieve_tablet(
                teller_username=self.current_user.user_info.username,
                session=self.oracle_session
            )
        )
        if not tablet_info['tablet_id'] or not tablet_info['is_paired']:
            return self.response_exception(msg=ERROR_TABLET_IS_NOT_PAIRED)

        action = request.action
        extra_data = request.extra_data
        data = {}

        # trường hợp khách hàng không nhập số giấy tờ định danh mà bảo gdv giao dịch thẳng
        # -> Tự động tạo booking authentication
        # trường hợp khách hàng đã nhập số giấy tờ định danh
        # -> Lấy thông tin booking authentication đã tạo ở bước nhập ra
        booking_authentication = self.call_repos(
            await repos_retrieve_and_init_if_not_found_booking_authentication(
                tablet_id=tablet_info['tablet_id'],
                teller_username=self.current_user.user_info.username,
                session=self.oracle_session
            )
        )

        if action == MOBILE_ACTION_PROCESS_TRANSACTION:
            # check extra data
            try:
                TabletActionProcessingTransactionExtraData(**extra_data)
            except ValidationError:
                return self.response_exception(msg='', detail='Check transaction_name & booking_id in extra_data again')

            # check exist thì đáng lý return bên repo đó luôn nhưng code các phần khác như vậy nên để lại
            booking = self.call_repos(
                await repos_check_exist_booking(
                    booking_id=extra_data['booking_id'],
                    session=self.oracle_session
                )
            )
            if not booking:
                return self.response_exception(msg=ERROR_BOOKING_ID_NOT_EXIST, loc='booking_id')

            # khách hàng thực hiện 2 giao dịch
            # -> giao dịch trước thì booking_id đã được lưu, giao dịch sau thì clone 1 dòng booking_authentication
            if booking_authentication.booking_id and booking_authentication.booking_id != extra_data['booking_id']:
                self.call_repos(
                    await repos_init_booking_authentication(
                        tablet_id=booking_authentication.tablet_id,
                        teller_username=booking_authentication.teller_username,
                        identity_number=booking_authentication.identity_number,
                        cif_number=booking_authentication.cif_number,
                        session=self.oracle_session,
                        identity_front_document_file_uuid=booking_authentication.identity_front_document_file_uuid,
                        identity_front_document_file_uuid_ekyc=booking_authentication.identity_front_document_file_uuid_ekyc,
                        face_file_uuid=booking_authentication.face_file_uuid,
                        face_file_uuid_ekyc=booking_authentication.face_file_uuid_ekyc,
                        booking_id=extra_data['booking_id'],
                    )
                )
            else:
                booking_authentication.booking_id = extra_data['booking_id']

                self.call_repos(
                    await repos_update_current_booking_authentication_by_tablet_id(
                        need_to_update_booking_authentication=booking_authentication,
                        session=self.oracle_session
                    )
                )

            avatar_uuid_and_full_name = self.call_repos(
                await repos_get_customer_avatar_url_and_full_name_if_exist_by_booking_authentication_id(
                    booking_authentication_id=booking_authentication.id,
                    session=self.oracle_session
                )
            )
            if avatar_uuid_and_full_name['avatar_uuid']:
                avatar_url = self.call_repos(await repos_download_file(avatar_uuid_and_full_name['avatar_uuid']))
            else:
                avatar_url = None

            data['customer_info'] = {
                'avatar_url': f"{INIT_SERVICE['crm_app_url']}{avatar_url['file_url']}" if avatar_url else None,
                'full_name': avatar_uuid_and_full_name['full_name'],
                'rank_type_id': None,  # TODO: rank id khách hàng hiện tại
                'rank_type_name': None  # TODO: rank name khách hàng hiện tại
            }
            data['transaction_name'] = extra_data['transaction_name']
        elif action == MOBILE_ACTION_NEW_TRANSACTION:
            avatar_uuid_and_full_name = self.call_repos(
                await repos_get_customer_avatar_url_and_full_name_if_exist_by_booking_authentication_id(
                    booking_authentication_id=booking_authentication.id,
                    session=self.oracle_session
                )
            )
            if avatar_uuid_and_full_name['avatar_uuid']:
                avatar_url = self.call_repos(await repos_download_file(avatar_uuid_and_full_name['avatar_uuid']))
            else:
                avatar_url = None

            data['customer_info'] = {
                'avatar_url': f"{INIT_SERVICE['crm_app_url']}{avatar_url['file_url']}" if avatar_url else None,
                'full_name': avatar_uuid_and_full_name['full_name'],
                'rank_type_id': None,  # TODO: rank id khách hàng hiện tại
                'rank_type_name': None  # TODO: rank name khách hàng hiện tại
            }
            data['transaction_name'] = None

        elif action == MOBILE_ACTION_SIGN:
            # check extra data
            try:
                TabletActionSignExtraData(**extra_data)
            except ValidationError:
                return self.response_exception(msg='', detail='Check documents in extra_data again')

            data['documents'] = extra_data['documents']

        elif action == MOBILE_ACTION_TAKE_DOCUMENT_PHOTO or action == MOBILE_ACTION_TAKE_FACE_PHOTO:
            data['is_identify_customer_step'] = False

        # gửi cho mobile message thông báo chuyển screen
        service_rabbitmq.publish(
            message={
                "action": action,
                "data": data
            },
            routing_key=get_topic_name(
                device_type=DEVICE_TYPE_MOBILE,
                tablet_id=tablet_info['tablet_id'],
                otp=tablet_info['otp']
            )
        )

        return self.response({
            'status': True
        })
