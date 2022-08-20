from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.mobile.repository import repos_pair_by_otp
from app.api.v1.endpoints.tablet.mobile.schema import (
    ListBannerLanguageCodeQueryParam, SyncWithWebByOTPRequest
)
from app.settings.event import service_idm, service_rabbitmq, service_redis
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, LIST_BANNER_LANGUAGE_CODE_ENGLISH,
    LIST_BANNER_LANGUAGE_CODE_VIETNAMESE, LIST_BANNER_LANGUAGE_NAME_ENGLISH,
    LIST_BANNER_LANGUAGE_NAME_VIETNAMESE, WEB_ACTION_PAIRED
)
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
