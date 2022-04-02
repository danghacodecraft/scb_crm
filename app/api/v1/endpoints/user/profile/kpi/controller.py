from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.kpi.repository import repos_kpi


class CtrKpi(BaseController):
    async def ctr_kpi(self, employee_id: str):
        is_success, kpi = self.call_repos(
            await repos_kpi(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            self.response_exception(msg=str(kpi))

        return self.response_paging(data=kpi)
