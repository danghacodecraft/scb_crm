from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.repository import repos_profile
from app.utils.address_functions.functions import combine_full_address
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_DWH, MESSAGE_STATUS, USER_NOT_EXIST
)


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
        is_success, profile = self.call_repos(
            await repos_profile(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )

        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_DWH, loc="EMP_DETAIL", detail=str(profile))

        number_and_street = profile['curriculum_vitae']['contact']['contact']['address']
        ward = profile['curriculum_vitae']['contact']['contact']['ward']
        district = profile['curriculum_vitae']['contact']['contact']['district']
        province = profile['curriculum_vitae']['contact']['contact']['province']

        profile = {
            "avatar": profile['avatar'],
            "gender": profile['curriculum_vitae']['individual']['gender'],
            "full_name_vn": profile['emp_name'],
            "address": combine_full_address(
                number_and_street=number_and_street,
                ward=ward,
                district=district,
                province=province
            ),
            "user_name": profile['email'].split("@SCB.COM.VN")[0],
            "email": profile['email'],
            "mobile_number": profile['mobile'],
            "code": profile['emp_id'],
            "department": profile['dep_name'],
            "titles": profile['title'],
            "manager": profile['manager'],
            "telephone_number": None
        }

        return self.response(data=profile)
