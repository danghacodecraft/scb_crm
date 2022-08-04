from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT,
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import date_string_to_other_date_string_format


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

        foreign = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))

        foreign_info = foreign[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT]["data_output"][
            "employee_info"]['language_info_item']

        certification_date = date_string_to_other_date_string_format(
            date_input=foreign_info['english_issue_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )
        response_foreign = [dict(
            language_type=foreign_info['english'],
            level=foreign_info['english_level'],
            gpa=foreign_info['english_mark'],
            certification_date=certification_date
        )]

        return self.response(data=response_foreign)
