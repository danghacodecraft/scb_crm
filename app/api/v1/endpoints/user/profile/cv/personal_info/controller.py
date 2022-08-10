from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    MaritalStatus, Religion
)
from app.utils.constant.cif import CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT,
    GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT, GW_GENDER_FEMALE,
    GW_GENDER_MALE
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import date_string_to_other_date_string_format


class CtrPersonalInfo(BaseController):
    async def ctr_personal_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        personal_info = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))
        employee_info = personal_info[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT]["data_output"]["employee_info"]

        identity_info = employee_info['id_info']

        date_of_birth = date_string_to_other_date_string_format(
            date_input=employee_info['birth_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        gender_code_or_name = employee_info["sex"]

        if gender_code_or_name == GW_GENDER_MALE:
            gender_code_or_name = CRM_GENDER_TYPE_MALE
        if gender_code_or_name == GW_GENDER_FEMALE:
            gender_code_or_name = CRM_GENDER_TYPE_FEMALE

        dropdown_gender = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name
        )

        identity_issued_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_issued_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        identity_expired_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        dropdown_place_of_birth = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=Religion, name=employee_info['birth_province']
        )
        dropdown_religion = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=Religion, name=employee_info['religion']
        )
        dropdown_nationality = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=AddressCountry, name=employee_info['nationality']
        )

        dropdown_marital_status = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=MaritalStatus, name=employee_info['marital_status']
        )
        dropdown_id_issued_location = await self.dropdown_mapping_crm_model_or_dropdown_name(
            model=PlaceOfIssue, name=identity_info['id_issued_location']
        )

        response_personal_info = {
            "date_of_birth": date_of_birth,
            "place_of_birth": dropdown_place_of_birth,
            "gender": dropdown_gender,
            "ethnic": {
                "id": "KINH",
                "code": "KINH",
                "name": "Kinh"    # Todo Dân tộc không tìm thấy
            },
            "religion": dropdown_religion,
            "nationality": dropdown_nationality,
            "marital_status": dropdown_marital_status,
            "identity_number": identity_info['id_num'],
            "issued_date": identity_issued_date,
            "expired_date": identity_expired_date,
            "place_of_issue": dropdown_id_issued_location
        }

        return self.response(data=response_personal_info)
