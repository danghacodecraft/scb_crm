from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.card_works.repository import (
    repos_gw_open_cards
)
from app.utils.constant.gw import GW_FUNC_OPEN_CARDS_OUT
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


class CtrGWCardWorks(BaseController):
    async def ctr_gw_open_cards(self, data):
        is_success, gw_card_works = self.call_repos(await repos_gw_open_cards(
            current_user=self.current_user.user_info,
            data=data
        ))

        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_card_works))

        response_data = gw_card_works[GW_FUNC_OPEN_CARDS_OUT]['data_output']

        return self.response(data=response_data)
