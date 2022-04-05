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

        response_it = [dict(
            certification=None,
            level=None,
            gpa=None
        )]
        if it:
            response_it = []
            if it:
                it = it['level']['information_technology']
                response_it.append({
                    "certification": it['certificate'],
                    "level": it['level'],
                    "gpa": it['mark']
                })

        return self.response(data=response_it)
