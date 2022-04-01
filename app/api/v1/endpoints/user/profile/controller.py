from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.repository import repos_profile


class CtrProfile(BaseController):
    async def ctr_profile(self):
        profile = self.call_repos(
            await repos_profile(
                session=self.oracle_session
            )
        )

        return self.response(data=profile)
