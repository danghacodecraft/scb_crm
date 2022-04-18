from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.foreign.repository import (
    repos_foreign
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrForeign(BaseController):
    async def ctr_foreign(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, foreign = self.call_repos(
            await repos_foreign(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )

        if not is_success:
            return self.response_exception(msg=str(foreign))

        response_foreign = []
        foreign_language = foreign['level']['foreign_language']
        if foreign_language['certificate'] and foreign_language['level'] and foreign_language['mark'] and foreign_language['mark']:
            response_foreign = [dict(
                language_type=foreign_language['certificate'],
                level=foreign_language['level'],
                gpa=foreign_language['mark'],
                certification_date=foreign_language['mark']
            )]

        return self.response(data=response_foreign)
