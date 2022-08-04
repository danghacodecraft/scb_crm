from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.utils.constant.gw import GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT
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

        it = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))

        it_infos = it[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT]["data_output"][
            "employee_info"]['certificate_info_list']['certificate_info_item']

        response_it = [{
            "certification": it_info['it_certificate'],
            "level": it_info['it_certificate_level'],
            "gpa": "8"
        } for it_info in it_infos]

        return self.response(data=response_it)
