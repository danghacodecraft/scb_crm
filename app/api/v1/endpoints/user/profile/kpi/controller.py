from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.kpi.repository import repos_kpi


class CtrKpi(BaseController):
    async def ctr_kpi(self):
        kpi = self.call_repos(
            await repos_kpi(
                session=self.oracle_session
            )
        )

        return self.response_paging(data=kpi)
