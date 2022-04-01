from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.repository import repos_profile
from app.settings.event import service_dwh


class CtrProfile(BaseController):
    async def ctr_profile(self, employee_id: str):
        is_success, data = await service_dwh.detail(employee_id=employee_id)
        profile = self.call_repos(
            await repos_profile(
                session=self.oracle_session
            )
        )

        return self.response(data=profile)
