from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.felicitation.repository import (
    repos_felicitation
)


class CtrFelicitation(BaseController):
    async def ctr_felicitation(self):
        felicitation = self.call_repos(
            await repos_felicitation(
                session=self.oracle_session
            )
        )

        return self.response_paging(data=felicitation)
