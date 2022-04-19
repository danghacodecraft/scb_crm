from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.contact.repository import repo_contact


class CtrContact(BaseController):
    async def ctr_contact(self, code):

        contact = self.call_repos(
            await repo_contact(
                code=code,
                session=self.oracle_session_task
            )
        )

        return self.response(data=contact)
