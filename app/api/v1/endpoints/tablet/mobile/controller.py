from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.mobile.repository import repos_pair_by_otp
from app.api.v1.endpoints.tablet.mobile.schema import SyncWithWebByOTPRequest
from app.utils.constant.tablet import DEVICE_TYPE_MOBILE
from app.utils.tablet_functions import get_broker_mqtt_info, get_topic_name


class CtrTabletMobile(BaseController):
    async def sync_with_web_by_otp(self, request: SyncWithWebByOTPRequest):
        tablet_info = self.call_repos(
            await repos_pair_by_otp(
                otp=request.otp,
                device_information=str(request.device_info.json()),
                session=self.oracle_session
            )
        )

        mqtt_info = get_broker_mqtt_info()
        topic_name = get_topic_name(
            device_type=DEVICE_TYPE_MOBILE,
            tablet_id=tablet_info['tablet_id'],
            otp=request.otp
        )
        mqtt_info['topic_name'] = topic_name

        # TODO: send to mqtt message

        return self.response({
            'mqtt_info': mqtt_info,
            'token': topic_name,
        })
