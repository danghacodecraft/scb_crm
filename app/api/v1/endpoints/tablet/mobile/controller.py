from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.mobile.repository import repos_pair_by_otp
from app.api.v1.endpoints.tablet.mobile.schema import SyncWithWebByOTPRequest
from app.settings.event import service_rabbitmq
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, WEB_ACTION_PAIRED
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

        return self.response({
            'mqtt_info': mqtt_info,
            'token': topic_name,
        })
