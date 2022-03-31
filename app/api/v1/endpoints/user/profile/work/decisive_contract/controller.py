from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.decisive_contract.repository import (
    repos_decisive_contract
)


class CtrDecisiveContract(BaseController):
    async def ctr_decisive_contract(self):
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        decisive_contract = self.call_repos(
            await repos_decisive_contract(
                session=self.oracle_session
            )
        )

        return self.response(data=decisive_contract)
