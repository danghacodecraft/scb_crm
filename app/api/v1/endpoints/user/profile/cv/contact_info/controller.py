from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.cv.contact_info.repository import (
    repos_contact_info
)


class CtrContact_Info(BaseController):
    async def ctr_contact_info(self):
        # self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))
        contact_info = self.call_repos(
            await repos_contact_info(
                session=self.oracle_session
            )
        )

        return self.response(data=contact_info)
