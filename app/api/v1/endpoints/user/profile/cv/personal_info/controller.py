from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.cv.personal_info.repository import (
    repos_personal_info
)


class CtrPersonalInfo(BaseController):
    async def ctr_personal_info(self):
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        personal_info = self.call_repos(
            await repos_personal_info(
                session=self.oracle_session
            )
        )

        return self.response(data=personal_info)
