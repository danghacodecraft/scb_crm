from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.discipline.repository import (
    repos_discipline
)


class CtrDiscipline(BaseController):
    async def ctr_discipline(self):
        discipline = self.call_repos(
            await repos_discipline(
                session=self.oracle_session
            )
        )

        return self.response_paging(data=discipline)
