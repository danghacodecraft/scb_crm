from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.kpi.repository import repos_kpi


class CtrKpi(BaseController):
    async def ctr_kpi(self, employee_id: str):
        is_success, kpis = self.call_repos(
            await repos_kpi(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(kpis))

        return self.response_paging(data=[
            {
                "assessment_period": kpi["DATE"],
                "total_score": kpi["KPI"],
                "completion_rate": kpi["PER"],
                "result": kpi["RES"],
                "note": kpi["NOTE"]
            } for kpi in kpis
        ])
