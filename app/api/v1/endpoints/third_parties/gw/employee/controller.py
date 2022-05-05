from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code,
    repos_gw_get_employee_info_from_user_name
)


class CtrGWEmployee(BaseController):
    async def ctr_gw_get_employee_info_from_code(
            self,
            employee_code: str
    ):
        current_user = self.current_user
        gw_employee_info = self.call_repos(await repos_gw_get_employee_info_from_code(
            employee_code=employee_code,
            current_user=current_user
        ))

        employee_info = gw_employee_info["selectEmployeeInfoFromCode_out"]["data_output"]["employee_info"]

        return self.response(data=dict(
            staff_code=employee_info['staff_code'],
            staff_name=employee_info['staff_name'],
            fullname_vn=employee_info['full_name'],
            work_location=employee_info['work_location'],
            email=employee_info['email_scb'],
            contact_mobile=employee_info['contact_mobile'],
            internal_mobile=employee_info['internal_mobile'],
            title_code=employee_info['title_code'],
            title_name=employee_info['title_name'],
            branch_org=employee_info['branch_org'],
            avatar=employee_info['avatar'],
        ))

    async def ctr_gw_get_employee_info_from_user_name(
            self,
            employee_name: str
    ):
        current_user = self.current_user
        gw_employee_info = self.call_repos(await repos_gw_get_employee_info_from_user_name(
            employee_name=employee_name,
            current_user=current_user
        ))

        employee_info = gw_employee_info["selectEmployeeInfoFromUserName_out"]["data_output"]["employee_info"]

        return self.response(data=dict(
            staff_code=employee_info['staff_code'],
            staff_name=employee_info['staff_name'],
            fullname_vn=employee_info['full_name'],
            work_location=employee_info['work_location'],
            email=employee_info['email_scb'],
            contact_mobile=employee_info['contact_mobile'],
            internal_mobile=employee_info['internal_mobile'],
            title_code=employee_info['title_code'],
            title_name=employee_info['title_name'],
            branch_org=employee_info['branch_org'],
            avatar=employee_info['avatar'],
        ))
