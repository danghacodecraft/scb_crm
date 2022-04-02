from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.discipline.repository import (
    repos_discipline
)


class CtrDiscipline(BaseController):
    async def ctr_discipline(self, employee_id: str):
        is_success, discipline = self.call_repos(
            await repos_discipline(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            self.response_exception(msg=str(discipline))

        return self.response_paging(data=discipline)
