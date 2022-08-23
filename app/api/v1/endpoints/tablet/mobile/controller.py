from fastapi import UploadFile
from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.file.repository import (
    repos_download_file, repos_upload_file
)
from app.api.v1.endpoints.file.validator import file_validator
from app.api.v1.endpoints.tablet.mobile.repository import (
    repos_init_booking_authentication, repos_pair_by_otp,
    repos_retrieve_current_booking_authentication_by_tablet_id,
    repos_retrieve_table_by_tablet_token,
    repos_update_current_booking_authentication_by_tablet_id
)
from app.api.v1.endpoints.tablet.mobile.schema import (
    ListBannerLanguageCodeQueryParam, SubmitCustomerIdentityNumberRequest,
    SyncWithWebByOTPRequest
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_customer_avatar_url_from_cif, repos_gw_get_customer_info_list
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import INIT_SERVICE, service_rabbitmq, service_redis
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, LIST_BANNER_LANGUAGE_CODE_ENGLISH,
    LIST_BANNER_LANGUAGE_CODE_VIETNAMESE, LIST_BANNER_LANGUAGE_NAME_ENGLISH,
    LIST_BANNER_LANGUAGE_NAME_VIETNAMESE,
    MOBILE_ACTION_ENTER_IDENTITY_NUMBER_FAIL,
    MOBILE_ACTION_TAKE_DOCUMENT_PHOTO, MOBILE_ACTION_TAKE_FACE_PHOTO,
    WEB_ACTION_FOUND_CUSTOMER, WEB_ACTION_NOT_FOUND_CUSTOMER,
    WEB_ACTION_PAIRED, WEB_ACTION_RECEIVED_PHOTO
)
from app.utils.error_messages import ERROR_TABLET_INVALID_TOKEN
from app.utils.functions import now
from app.utils.tablet_functions import (
    get_client_broker_config_info, get_topic_name
)


class CtrTabletMobile(BaseController):
    async def sync_with_web_by_otp(self, request: SyncWithWebByOTPRequest):
        tablet_info = self.call_repos(
            await repos_pair_by_otp(
                otp=request.otp,
                device_information=str(request.device_info.json()),
                session=self.oracle_session
            )
        )

        mqtt_info = get_client_broker_config_info(device_type=DEVICE_TYPE_MOBILE)
        topic_name = get_topic_name(
            device_type=DEVICE_TYPE_MOBILE,
            tablet_id=tablet_info['tablet_id'],
            otp=request.otp
        )
        mqtt_info['topic_name'] = topic_name

        # gửi cho web message thông báo paired thành công
        service_rabbitmq.publish(
            message={
                "action": WEB_ACTION_PAIRED,
                "data": {}
            },
            routing_key=get_topic_name(
                device_type=DEVICE_TYPE_WEB,
                tablet_id=tablet_info['tablet_id'],
                otp=request.otp
            )
        )

        teller_user_info = (await service_redis.get(tablet_info['teller_username']))['user_info']

        return self.response({
            'mqtt_info': mqtt_info,
            'token': topic_name,
            'branch_name': teller_user_info['hrm_branch_name'],
            'languages': [
                {
                    'language_code': LIST_BANNER_LANGUAGE_CODE_VIETNAMESE,
                    'language_name': LIST_BANNER_LANGUAGE_NAME_VIETNAMESE
                },
                {
                    'language_code': LIST_BANNER_LANGUAGE_CODE_ENGLISH,
                    'language_name': LIST_BANNER_LANGUAGE_NAME_ENGLISH
                },
            ],
            'teller_info': {
                'avatar_url': f"{INIT_SERVICE['crm_app_url']}{teller_user_info['avatar_url']}",
                'full_name': teller_user_info['name'],
            }
        })

    async def list_banner(self, language_code: ListBannerLanguageCodeQueryParam):
        """
        tablet_banner_share_link = https://fileshare.scb.com.vn/d/a398af9d54d044169375/
        thumbnail = https://fileshare.scb.com.vn/thumbnail/a398af9d54d044169375/1920/TiengAnh/BaoHiem/KienTaoThinhVuong%404x-80.jpg
        """
        language_relative_path = 'TiengViet' if language_code == ListBannerLanguageCodeQueryParam.vi else 'TiengAnh'
        tablet_banner_share_link = INIT_SERVICE['fileshare']['tablet_banner_share_link']
        tablet_banner_thumbnail_link = f"{tablet_banner_share_link.replace('/d/', '/thumbnail/')}1920/{language_relative_path}/"

        # TODO: get all files in folder instead of hard file name
        return self.response([
            {
                "category_name": "Thẻ" if language_code == ListBannerLanguageCodeQueryParam.vi else 'Card',
                "image_urls": [
                    f'{tablet_banner_thumbnail_link}The/BeYOU@4x-80.jpg',
                    f'{tablet_banner_thumbnail_link}The/PhatHanhNgay-QuaTraoTay@4x-80.jpg'
                ]
            },
            {
                "category_name": "Tiết kiệm" if language_code == ListBannerLanguageCodeQueryParam.vi else 'Saving',
                "image_urls": [
                    f'{tablet_banner_thumbnail_link}TietKiem/TKOL@4x-80.jpg'
                ]
            },
            {
                "category_name": "Vay" if language_code == ListBannerLanguageCodeQueryParam.vi else 'Loan',
                "image_urls": [
                    f'{tablet_banner_thumbnail_link}Vay/Home%20in%20hand%404x-80.jpg'
                ]
            },
            {
                "category_name": "Bảo hiểm" if language_code == ListBannerLanguageCodeQueryParam.vi else 'Insurance',
                "image_urls": [
                    f'{tablet_banner_thumbnail_link}BaoHiem/KienTaoThinhVuong@4x-80.jpg'
                ]
            },
            {
                "category_name": "TK thanh toán" if language_code == ListBannerLanguageCodeQueryParam.vi else 'Payment account',
                "image_urls": [
                    f'{tablet_banner_thumbnail_link}TaiKhoanThanhToan/S-Digital@4x-80.jpg'
                ]
            }
        ])

    async def _check_tablet_token(self, tablet_token):
        try:
            device_type, tablet_id_and_otp = tablet_token.split('.')
            tablet_id = tablet_id_and_otp[:-6]
            otp = tablet_id_and_otp[-6:]
        except Exception:
            return self.response_exception(
                msg=ERROR_TABLET_INVALID_TOKEN, error_status_code=status.HTTP_401_UNAUTHORIZED
            )

        if device_type != DEVICE_TYPE_MOBILE:
            return self.response_exception(
                msg=ERROR_TABLET_INVALID_TOKEN, error_status_code=status.HTTP_401_UNAUTHORIZED
            )

        result_tablet = self.call_repos(
            await repos_retrieve_table_by_tablet_token(
                tablet_id=tablet_id,
                otp=otp,
                session=self.oracle_session
            )
        )

        return {
            'tablet_id': result_tablet['tablet_id'],
            'teller_username': result_tablet['teller_username'],
            'otp': result_tablet['otp']
        }

    async def submit_customer_identity_number(self, tablet_token: str, request: SubmitCustomerIdentityNumberRequest):
        tablet_info = await self._check_tablet_token(tablet_token=tablet_token)

        teller_info = await service_redis.get(tablet_info['teller_username'])
        teller_user = AuthResponse(**teller_info)

        cif_number = None
        customer_info_list = self.call_repos(await repos_gw_get_customer_info_list(
            cif_number='',
            identity_number=request.customer_identity_number,
            mobile_number='',
            full_name='',
            current_user=teller_user
        ))
        customer_list = customer_info_list["selectCustomerRefDataMgmtCIFNum_out"]["data_output"]["customer_list"]

        if len(customer_list) == 1:
            found_customer_info = customer_list[0]['customer_info_item']['customer_info']

            cif_number = found_customer_info['cif_info']['cif_num']

            avatar_uuid = self.call_repos(
                await repos_get_customer_avatar_url_from_cif(
                    cif_number=cif_number,
                    session=self.oracle_session
                )
            )
            avatar_url = self.call_repos(await repos_download_file(avatar_uuid))

            # gửi cho web message thông báo tìm thấy khách hàng
            service_rabbitmq.publish(
                message={
                    "action": WEB_ACTION_FOUND_CUSTOMER,
                    "data": {
                        "customer_identity_number": request.customer_identity_number,
                        "customer_info": {
                            "cif_num": cif_number,
                            "full_name": found_customer_info['full_name'],
                            "avatar_url": f"{INIT_SERVICE['crm_app_url']}{avatar_url['file_url']}" if avatar_url else None
                        }
                    }
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_WEB,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )

            # gửi cho mobile message thông báo chụp ảnh giấy tờ (kèm cờ để truy vấn giao dịch sau này)
            service_rabbitmq.publish(
                message={
                    "action": MOBILE_ACTION_TAKE_DOCUMENT_PHOTO,
                    "data": {
                        "is_identify_customer_step": True
                    }
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_MOBILE,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )
        else:
            # gửi cho web message thông báo không tìm thấy khách hàng
            service_rabbitmq.publish(
                message={
                    "action": WEB_ACTION_NOT_FOUND_CUSTOMER,
                    "data": {
                        "customer_identity_number": request.customer_identity_number,
                        "customer_info": {
                            "cif_num": None,
                            "full_name": None,
                            "avatar_url": None
                        }
                    }
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_WEB,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )

            # gửi cho mobile message thông báo số giấy tờ định danh sai
            service_rabbitmq.publish(
                message={
                    "action": MOBILE_ACTION_ENTER_IDENTITY_NUMBER_FAIL,
                    "data": {}
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_MOBILE,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )

        self.call_repos(
            await repos_init_booking_authentication(
                tablet_id=tablet_info['tablet_id'],
                teller_username=tablet_info['teller_username'],
                identity_number=request.customer_identity_number,
                cif_number=cif_number,
                session=self.oracle_session
            )
        )

        return self.response(data={
            'status': True
        })

    async def take_photo(self, tablet_token: str, is_identify_customer_step: bool, file_upload: UploadFile):
        tablet_info = await self._check_tablet_token(tablet_token=tablet_token)

        booking_authentication = self.call_repos(
            await repos_retrieve_current_booking_authentication_by_tablet_id(
                tablet_id=tablet_info['tablet_id'],
                session=self.oracle_session
            )
        )

        if not is_identify_customer_step and (
                not booking_authentication.identity_front_document_file_uuid or not booking_authentication.face_file_uuid):
            return self.response_exception(
                msg="INVALID_IS_IDENTIFY_CUSTOMER_STEP", detail="Customer has not taken an authentic photo"
            )
        elif is_identify_customer_step and booking_authentication.identity_front_document_file_uuid and booking_authentication.face_file_uuid:
            return self.response_exception(
                msg="INVALID_IS_IDENTIFY_CUSTOMER_STEP", detail="Customer has taken authentic photos before"
            )

        data_file_upload = await file_upload.read()

        self.call_validator(await file_validator(data_file_upload))

        is_success, info_file = self.call_repos(await repos_upload_file(
            file=data_file_upload,
            name=file_upload.filename,
            ekyc_flag=True,
            save_to_db_flag=False,
            booking_id=None,
            current_user=None
        ))
        if not is_success:
            return self.response_exception(msg="ERROR_INSERT_DOCUMENT_FILE", detail=str(info_file))

        info_file['created_at'] = now()

        if is_identify_customer_step:
            if not booking_authentication.identity_front_document_file_uuid:
                booking_authentication.identity_front_document_file_uuid = info_file['uuid']
                booking_authentication.identity_front_document_file_uuid_ekyc = info_file['uuid_ekyc']

                # gửi cho mobile message thông báo chụp ảnh khuôn mặt (kèm cờ để truy vấn giao dịch sau này)
                service_rabbitmq.publish(
                    message={
                        "action": MOBILE_ACTION_TAKE_FACE_PHOTO,
                        "data": {
                            "is_identify_customer_step": True
                        }
                    },
                    routing_key=get_topic_name(
                        device_type=DEVICE_TYPE_MOBILE,
                        tablet_id=tablet_info['tablet_id'],
                        otp=tablet_info['otp']
                    )
                )
            elif not booking_authentication.face_file_uuid:
                booking_authentication.face_file_uuid = info_file['uuid']
                booking_authentication.face_file_uuid_ekyc = info_file['uuid_ekyc']

            self.call_repos(
                await repos_update_current_booking_authentication_by_tablet_id(
                    need_to_update_booking_authentication=booking_authentication,
                    session=self.oracle_session
                )
            )
        else:
            # gửi cho web message thông báo đã chụp ảnh thành công
            service_rabbitmq.publish(
                message={
                    "action": WEB_ACTION_RECEIVED_PHOTO,
                    "data": info_file
                },
                routing_key=get_topic_name(
                    device_type=DEVICE_TYPE_WEB,
                    tablet_id=tablet_info['tablet_id'],
                    otp=tablet_info['otp']
                )
            )

        return self.response(data={
            'status': True
        })
