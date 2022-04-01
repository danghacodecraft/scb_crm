from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.repository import repos_profile


class CtrProfile(BaseController):
    async def ctr_profile(self, employee_id: str):

        is_success, profile = self.call_repos(
            await repos_profile(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            self.response_exception(msg=str(profile))

        return self.response(data=profile)
