from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_retrieve_employee_info_from_code
)
from app.utils.constant.gw import GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrEducation(BaseController):
    async def ctr_education(self, ):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        education = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=employee_id, current_user=self.current_user
        ))

        education_info = education[GW_FUNC_RETRIEVE_EMPLOYEE_INFO_FROM_CODE_OUT]["data_output"][
            "employee_info"]['education_info']

        return self.response(data={
            "education_information": education_info['academy'],
            "education_level": education_info['education_level'],
            "professional": education_info['education_skill'],
            "major": education_info['major'],
            "school": education_info['school_name'],
            "training_method": education_info['training_form'],
            "ranking": education_info['degree'],
            "gpa": education_info['gpa']
        })
