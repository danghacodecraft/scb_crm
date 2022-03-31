from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.it.repository import repos_it


class CtrIt(BaseController):
    async def ctr_it(self):
        it = self.call_repos(
            await repos_it(
                session=self.oracle_session
            )
        )

        return self.response_paging(data=it)
