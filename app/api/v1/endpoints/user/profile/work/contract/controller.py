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


class CtrContract(BaseController):
    async def ctr_contract_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        contract = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))
        contract_info = contract[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT][
            "data_output"]["employee_info"]['contract_info']

        start_date = date_string_to_other_date_string_format(
            date_input=contract_info['contract_effected_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        end_date = date_string_to_other_date_string_format(
            date_input=contract_info['contract_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        addendum_start_date = date_string_to_other_date_string_format(
            date_input=contract_info['schedule_of_contract_effected_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        addendum_end_date = date_string_to_other_date_string_format(
            date_input=contract_info['schedule_of_contract_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        resign_date = date_string_to_other_date_string_format(
            date_input=contract_info['stop_job_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        response_contract = {
            "type": contract_info['contract_type'],
            "number": contract_info['contract_name'],
            "start_date": start_date,
            "end_date": end_date,
            "addendum": {
                "number": contract_info['schedule_of_contract_num'],
                "start_date": addendum_start_date,
                "end_date": addendum_end_date,
            },
            "resign_date": resign_date
        }

        return self.response(data=response_contract)
