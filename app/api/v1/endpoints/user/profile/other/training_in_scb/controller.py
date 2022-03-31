from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.training_in_scb.repository import (
    repos_training_in_scb
)


class CtrTrainingInSCB(BaseController):
    async def ctr_training_in_scb(selfs):
        training_in_scb = selfs.call_repos(
            await repos_training_in_scb(
                session=selfs.oracle_session
            )
        )

        return selfs.response_paging(data=training_in_scb)
