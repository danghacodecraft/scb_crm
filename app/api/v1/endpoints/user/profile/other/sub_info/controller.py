from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.sub_info.repository import (
    repos_sub_info
)


class Ctr_Sub_Info(BaseController):
    async def ctr_sub_info(self):
        sub_info = self.call_repos(
            await repos_sub_info(
                session=self.oracle_session
            )
        )

        return self.response(data=sub_info)
