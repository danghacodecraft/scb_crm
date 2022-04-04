from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.it.repository import repos_it


class CtrIt(BaseController):
    async def ctr_it(self, employee_id: str):
        is_success, it = self.call_repos(
            await repos_it(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(it))

        it = it['level']['information_technology']
        response_data = {
            "certification": it['certificate'],
            "level": it['level'],
            "gpa": it['mark']
        }

        return self.response_paging(data=response_data)
