from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.kpi.repository import repos_kpi
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrKpi(BaseController):
    async def ctr_kpi(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, kpis = self.call_repos(
            await repos_kpi(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(kpis))

        response_kpis = []
        if kpis:
            response_kpis = [
                {
                    "assessment_period": kpi["DATE"],
                    "total_score": kpi["KPI"],
                    "completion_rate": kpi["PER"],
                    "result": kpi["RES"],
                    "note": kpi["NOTE"]
                } for kpi in kpis
            ]
        return self.response(data=response_kpis)
