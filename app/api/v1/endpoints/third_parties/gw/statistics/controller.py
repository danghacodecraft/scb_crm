from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.statistics.repository import (
    repos_gw_select_statistic_banking_by_period
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


class CtrGWStatistic(BaseController):
    async def ctr_gw_select_statistic_banking_by_period(self, request):
        is_success, gw_select_statistic_banking_by_period = self.call_repos(await repos_gw_select_statistic_banking_by_period(
            from_date=request.from_date,
            to_date=request.to_date,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_statistic_banking_by_period))
        return self.response(data=gw_select_statistic_banking_by_period['SelectStatisticBankingByPeriod_out']['data_output'])
