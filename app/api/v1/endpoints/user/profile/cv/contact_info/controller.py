from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.utils.constant.gw import GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrContact_Info(BaseController):
    async def ctr_contact_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        contact = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))

        address_info = contact[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT][
            "data_output"]["employee_info"]['address_info']

        response_contact_info = {
            "contact_info": {
                "domicile": {
                    "number_and_street": address_info['original_address_line'],
                    "nationality": address_info['original_country'],
                    "province": address_info['original_city_name'],
                    "district": address_info['original_district_name'],
                    "ward": address_info['original_ward_name']
                },
                "resident": {
                    "number_and_street": address_info['line'],
                    "nationality": address_info['country_name'],
                    "province": address_info['city_name'],
                    "district": address_info['district_name'],
                    "ward": address_info['ward_name']
                },
                "temporary": {
                    "number_and_street": address_info['line'],
                    "nationality": address_info['country_name'],
                    "province": address_info['city_name'],
                    "district": address_info['district_name'],
                    "ward": address_info['ward_name']
                },
                "contact": {
                    "number_and_street": address_info['contact_address_line'],
                    "nationality": address_info['contact_address_country_name'],
                    "province": address_info['contact_address_city_name'],
                    "district": address_info['contact_address_district_name'],
                    "ward": address_info['contact_address_ward_name']
                }
            },
            "other_info": {
                "contact": {  # Todo Không có mối quan hệ
                    "relationship": "Cha ruột",
                    "mobile_number": "0944624977",
                    "contactor": "Trần Văn Đúng"
                },
                "guardian": {  # Todo Người bảo lãnh không tìm thấy
                    "guardian": "Nguyễn Xuân An",
                    "relationship": "Bạn bè",
                    "mobile_number": "0909125649"
                },
                "expiration_date": "2021-10-01"  # Todo Ngày hết hiệu lực
            }
        }

        return self.response(data=response_contact_info)
