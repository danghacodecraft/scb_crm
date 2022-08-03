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


class CtrWorkProfile(BaseController):
    async def ctr_work_profile_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        work_profile = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))
        employee_info = work_profile[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT][
            "data_output"]["employee_info"]

        work_profile_info = employee_info['profile_info']

        working_date = date_string_to_other_date_string_format(
            date_input=work_profile_info['join_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        probation_date = date_string_to_other_date_string_format(
            date_input=work_profile_info['probation_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        official_date = date_string_to_other_date_string_format(
            date_input=work_profile_info['official_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        seniority_date = date_string_to_other_date_string_format(
            date_input=work_profile_info['seniority_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        response_foreign = {
            "avatar": employee_info['avatar'],
            "working_date": working_date,
            "probationary_date": probation_date,
            "official_date": official_date,
            "current": {
                "branch": work_profile_info['department_info']['department_name'],
                "position": work_profile_info['jobtitle_name']
            },
            "root": {
                "branch": work_profile_info['org_department_info']['department_name'],
                "position": work_profile_info['jobtitle_name']
            },
            "temporary": {
                "branch": work_profile_info['temp_department_info']['department_name'],
                "position": work_profile_info['temp_jobtitle_name']
            },
            "seniority_date": seniority_date,
            "is_resident": work_profile_info['resident_status']
        }

        return self.response(data=response_foreign)
