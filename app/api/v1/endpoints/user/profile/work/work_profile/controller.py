from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.work_profile.repository import (
    repos_work_profile
)


class CtrWorkProfile(BaseController):
    async def ctr_work_profile(self):

        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        work_profile = self.call_repos(
            await repos_work_profile(
                session=self.oracle_session
            )
        )

        return self.response(data=work_profile)
