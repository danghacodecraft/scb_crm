from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.kpi.repository import repos_kpi
from app.utils.constant.gw import GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrKpi(BaseController):
    async def ctr_kpi(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_kpis = self.call_repos(await repos_kpi(current_user=current_user))

        kpis = gw_kpis[GW_FUNC_SELECT_KPIS_INFO_FROM_CODE_OUT]['data_output']['kpi_info_list']['kpi_info_item']
        response_kpis = []
        if kpis:
            response_kpis = [
                {
                    "assessment_period": kpi["period_name"],
                    "total_score": kpi["total_point"],
                    "completion_rate": kpi["kpi_completed"],
                    "result": kpi["grade_name"],
                    "note": kpi["kpi_note"]
                } for kpi in kpis
            ]
        return self.response(data=response_kpis)
