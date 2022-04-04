from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.cv.personal_info.repository import (
    repos_personal_info
)
from app.utils.constant.date_datetime import DATE_TYPE_DMY_WITH_SLASH
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrPersonalInfo(BaseController):
    async def ctr_personal_info(self, employee_id: str):
        is_success, personal_info = self.call_repos(
            await repos_personal_info(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(personal_info))
        date_of_birth = personal_info['curriculum_vitae']['individual']['birth_date']
        date_of_birth = datetime_to_date(string_to_datetime(date_of_birth, _format=DATE_TYPE_DMY_WITH_SLASH)) if date_of_birth else None

        issued_date = personal_info['curriculum_vitae']['individual']['passport']['issue_date']
        issued_date = datetime_to_date(string_to_datetime(issued_date)) if issued_date else None

        expired_date = personal_info['curriculum_vitae']['individual']['passport']['expire_date']
        expired_date = datetime_to_date(string_to_datetime(expired_date)) if expired_date else None

        personal_info = {
            "date_of_birth": date_of_birth,
            "place_of_birth": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['individual']['birth_province']
            },
            "gender": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['individual']['gender']
            },
            "ethnic": {
                "id": "1",
                "code": "Code",
                "name": "Kinh"    # Todo Dân tộc không tìm thấy
            },
            "religion": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['individual']['religion']
            },
            "nationality": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['contact']['temp']['nation']
            },
            "marital_status": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['individual']['marital']
            },
            "identity_number": personal_info['curriculum_vitae']['individual']['passport']['id'],
            "issued_date": issued_date,
            "expired_date": expired_date,
            "place_of_issue": {
                "id": "1",
                "code": "Code",
                "name": personal_info['curriculum_vitae']['individual']['passport']['issue_place']
            }
        }

        return self.response(data=personal_info)
