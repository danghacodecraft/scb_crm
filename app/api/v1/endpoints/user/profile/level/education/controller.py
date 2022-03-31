from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.education.repository import (
    repos_education
)


class CtrEducation(BaseController):
    async def ctr_education(self):
        education = self.call_repos(
            await repos_education(
                session=self.oracle_session
            )
        )

        return self.response(data=education)
