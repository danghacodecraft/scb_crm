from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.foreign.repository import (
    repos_foreign
)


class CtrForeign(BaseController):
    async def ctr_foreign(self, employee_id: str):
        is_success, foreign = self.call_repos(
            await repos_foreign(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )

        if not is_success:
            return self.response_exception(msg=str(foreign))
        foreign_language = foreign['level']['foreign_language']
        foreign = {
            "language_type": foreign_language['certificate'],
            "level": foreign_language['level'],
            "gpa": foreign_language['mark'],
            "certification_date": None   # Todo Ngày nhận chứng chỉ không tìm thấy
        }

        return self.response(data=foreign)
