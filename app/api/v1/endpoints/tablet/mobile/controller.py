from fastapi import UploadFile
from starlette import status

from app.api.base.controller import BaseController
from app.api.v1.endpoints.file.repository import repos_upload_file
from app.api.v1.endpoints.file.validator import file_validator
from app.api.v1.endpoints.tablet.mobile.repository import (
    repos_pair_by_otp, repos_retrieve_table_by_tablet_token
)
from app.api.v1.endpoints.tablet.mobile.schema import (
    ListBannerLanguageCodeQueryParam, SubmitCustomerIdentityNumberRequest,
    SyncWithWebByOTPRequest
)
from app.settings.event import service_idm, service_rabbitmq, service_redis
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, LIST_BANNER_LANGUAGE_CODE_ENGLISH,
    LIST_BANNER_LANGUAGE_CODE_VIETNAMESE, LIST_BANNER_LANGUAGE_NAME_ENGLISH,
    LIST_BANNER_LANGUAGE_NAME_VIETNAMESE, WEB_ACTION_PAIRED
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
            # TODO: check it
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
                # TODO: host name
                'avatar_url': service_idm.replace_with_cdn(teller_user_info['avatar_url']),
                'full_name': teller_user_info['name'],
            }
        })

    async def list_banner(self, language_code: ListBannerLanguageCodeQueryParam):
        # TODO: upload ảnh đến DMS và lấy link ở đây
        return self.response([
            {
                "category_name": "Thẻ",
                "image_urls": [
                    "https://fileshare.scb.com.vn/thumbnail/cba735e7d4b640539abb/2560/5c1ad7f20dc496797189ec7a6838b2158da10ada.jpg"
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
        # tablet_info = await self._check_tablet_token(tablet_token=tablet_token)
        await self._check_tablet_token(tablet_token=tablet_token)

        # TODO check request.customer_identity_number

        return self.response(data={
            'status': True
        })

    async def take_photo(self, tablet_token: str, is_identify_customer_step: bool, file_upload: UploadFile):
        # tablet_info = await self._check_tablet_token(tablet_token=tablet_token)
        await self._check_tablet_token(tablet_token=tablet_token)

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

        # TODO: is_identify_customer_step
        # if is_identify_customer_step:
        #     ...
        # else:
        #     ...

        return self.response(data={
            'status': True
        })
