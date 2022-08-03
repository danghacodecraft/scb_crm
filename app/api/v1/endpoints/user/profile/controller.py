from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.utils.address_functions.functions import combine_full_address
from app.utils.constant.cif import CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE
from app.utils.constant.gw import (
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT, GW_GENDER_FEMALE,
    GW_GENDER_MALE
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrProfile(BaseController):
    async def ctr_profile(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code
        profile = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))
        employee_info = profile[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT][
            "data_output"]["employee_info"]

        address_info = employee_info['address_info']

        gender_code_or_name = employee_info["sex"]
        if gender_code_or_name == GW_GENDER_MALE:
            gender_code_or_name = CRM_GENDER_TYPE_MALE
        if gender_code_or_name == GW_GENDER_FEMALE:
            gender_code_or_name = CRM_GENDER_TYPE_FEMALE

        dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name
        )

        profile = {
            "avatar": employee_info['avatar'],
            "gender": dropdown_gender,
            "full_name_vn": employee_info['full_name'],
            "address": combine_full_address(
                number_and_street=address_info['contact_address_line'],
                ward=address_info['contact_address_ward_name'],
                district=address_info['contact_address_district_name'],
                province=address_info['contact_address_city_name']
            ),
            "user_name": employee_info['staff_name'],
            "email": employee_info['email_scb'],
            "mobile_number": employee_info['contact_mobile'],
            "code": employee_info['staff_code'],
            "department": {
                "id": employee_info['department_info']['department_code'],
                "code": employee_info['department_info']['department_code'],
                "name": employee_info['department_info']['department_name']
            },
            "title": {
                "id": employee_info['title_code'],
                "code": employee_info['title_code'],
                "name": employee_info['title_name']
            },
            "manager": employee_info['direct_management'],
            "telephone_number": employee_info['internal_mobile']
        }

        return self.response(data=profile)
