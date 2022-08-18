from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.web.repository import repos_create_tablet_otp
from app.utils.constant.tablet import DEVICE_TYPE_WEB
from app.utils.tablet_functions import get_broker_mqtt_info, get_topic_name


class CtrTabletWeb(BaseController):
    async def ctr_get_otp_and_mqtt_info(self):
        otp_info = self.call_repos(
            await repos_create_tablet_otp(
                teller_username=self.current_user.user_info.username,
                session=self.oracle_session
            )
        )

        mqtt_info = get_broker_mqtt_info()
        mqtt_info['topic_name'] = get_topic_name(
            device_type=DEVICE_TYPE_WEB,
            tablet_id=otp_info['tablet_id'],
            otp=otp_info['otp']
        )

        return self.response({
            'otp_info': otp_info,
            'mqtt_info': mqtt_info
        })
