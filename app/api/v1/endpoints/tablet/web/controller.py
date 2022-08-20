from app.api.base.controller import BaseController
from app.api.v1.endpoints.tablet.web.repository import (
    repos_create_tablet_otp, repos_delete_tablet_if_exists,
    repos_retrieve_tablet
)
from app.api.v1.endpoints.user.repository import repos_get_username_from_token
from app.settings.event import service_rabbitmq
from app.utils.constant.tablet import (
    DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB, MOBILE_ACTION_UNPAIRED
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
