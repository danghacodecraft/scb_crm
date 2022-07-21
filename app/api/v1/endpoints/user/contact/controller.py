from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code
)
from app.third_parties.services.idm import ServiceIDM
from app.utils.constant.gw import GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT


class CtrContact(BaseController):
    async def ctr_contact(self, code):

        gw_contact = self.call_repos(
            await repos_gw_get_employee_info_from_code(current_user=self.current_user, employee_code=code)
        )
        contact = gw_contact[GW_FUNC_SELECT_EMPLOYEE_INFO_FROM_CODE_OUT]['data_output']
        employee_info = contact['employee_info']
        response_data = {
            "emp_name": employee_info["staff_name"],
            "emp_code": employee_info["staff_code"],
            "username": employee_info["email_scb"].split("@scb.com.vn")[0].upper(),
            "working_location": employee_info["work_location"],
            "email_scb": employee_info["email_scb"],
            "contact_mobile": employee_info["contact_mobile"],
            "internal_mobile": employee_info["internal_mobile"],
            "emp_id": "6036",
            "title_name": employee_info["title_name"],
            "unit": employee_info["branch_org"],
            "avatar_link": ServiceIDM().replace_with_cdn(employee_info["avatar"])
        }

        return self.response(data=response_data)
