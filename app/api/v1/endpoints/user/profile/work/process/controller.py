from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.process.repository import (
    repos_process
)


class CtrProcess(BaseController):
    async def ctr_process(self):
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        process = self.call_repos(
            await repos_process(
                session=self.oracle_session
            )
        )

        return self.response_paging(data=process)
