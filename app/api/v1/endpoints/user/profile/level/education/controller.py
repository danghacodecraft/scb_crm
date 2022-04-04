from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.education.repository import (
    repos_education
)


class CtrEducation(BaseController):
    async def ctr_education(self, employee_id: str):
        is_success, education = self.call_repos(
            await repos_education(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(education))
        education_cultural = education['level']['cultural']
        education = {
            "education_information": education_cultural['academy'],
            "education_level": education_cultural['education_level'],
            "professional": education_cultural['major'],  # TODO
            "major": education_cultural['major'],  # TODO
            "school": education_cultural['school'],
            "training_method": education_cultural['training'],
            "ranking": education_cultural['degree'],
            "gpa": None  # TODO Điểm tốt nghiệp không tìm thấy
        }

        return self.response(data=education)
