from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.contact.repository import repo_contact


class CtrContact(BaseController):
    async def ctr_contact(self):
        current_user = self.current_user.user_info

        contact = self.call_repos(
            await repo_contact(
                code=current_user.code,
                session=self.oracle_session_task
            )
        )

        return self.response(data=contact)
