from pydantic import ValidationError

from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.mobile.repository import (
    repos_retrieve_current_booking_authentication_by_tablet_id,
    repos_update_current_booking_authentication_by_tablet_id
)
from app.api.v1.endpoints.tablet.web.repository import (
    repos_create_tablet_otp, repos_delete_tablet_if_exists,
    repos_retrieve_tablet
)
from app.api.v1.endpoints.tablet.web.schema import (
    TabletActionProcessingTransactionExtraData, TabletActionSignExtraData,
    TabletSwitchScreenRequest
)
from app.api.v1.endpoints.user.repository import repos_get_username_from_token
from app.api.v1.others.booking.repository import repos_check_exist_booking
from app.settings.event import service_rabbitmq
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

        if action == MOBILE_ACTION_PROCESS_TRANSACTION:
            # check extra data
            try:
                TabletActionProcessingTransactionExtraData(**extra_data)
            except ValidationError:
                return self.response_exception(msg='', detail='Check transaction_name & booking_id in extra_data again')

            data['avatar_url'] = ''  # TODO: avatar khách hàng hiện tại
            data['rank_type_id'] = ''  # TODO: rank id khách hàng hiện tại
            data['rank_type_name'] = ''  # TODO: rank name khách hàng hiện tại
            data['transaction_name'] = extra_data['transaction_name']

            # check exist thì đáng lý return bên repo đó luôn nhưng code các phần khác như vậy nên để lại
            booking = self.call_repos(
                await repos_check_exist_booking(
                    booking_id=extra_data['booking_id'],
                    session=self.oracle_session
                )
            )
            if not booking:
                return self.response_exception(msg=ERROR_BOOKING_ID_NOT_EXIST, loc='booking_id')

            booking_authentication = self.call_repos(
                await repos_retrieve_current_booking_authentication_by_tablet_id(
                    tablet_id=tablet_info['tablet_id'],
                    session=self.oracle_session
                )
            )
            if not booking_authentication.identity_front_document_file_uuid or not booking_authentication.face_file_uuid:
                return self.response_exception(
                    msg="INVALID_IS_IDENTIFY_CUSTOMER_STEP", detail="Customer has not taken an authentic photo"
                )

            booking_authentication.booking_id = extra_data['booking_id']

            self.call_repos(
                await repos_update_current_booking_authentication_by_tablet_id(
                    need_to_update_booking_authentication=booking_authentication,
                    session=self.oracle_session
                )
            )
        elif action == MOBILE_ACTION_NEW_TRANSACTION:
            data['avatar_url'] = ''  # TODO: avatar khách hàng hiện tại
            data['rank_type_id'] = ''  # TODO: rank id khách hàng hiện tại
            data['rank_type_name'] = ''  # TODO: rank name khách hàng hiện tại
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
