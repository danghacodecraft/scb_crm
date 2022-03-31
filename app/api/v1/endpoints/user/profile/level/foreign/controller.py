from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.foreign.repository import (
    repos_foreign
)


class CtrForeign(BaseController):
    async def ctr_foreign(self):
        foreign = self.call_repos(
            await repos_foreign(
                session=self.oracle_session
            )
        )

        return self.response(data=foreign)
