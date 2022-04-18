from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.it.repository import repos_it
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrIt(BaseController):
    async def ctr_it(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, it = self.call_repos(
            await repos_it(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(it))

        response_it = []
        it = it['level']['information_technology']
        if it['certificate'] and it['level'] and it['mark']:
            response_it.append({
                "certification": it['certificate'],
                "level": it['level'],
                "gpa": it['mark']
            })

        return self.response(data=response_it)
