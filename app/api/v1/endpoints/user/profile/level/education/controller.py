from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.level.education.repository import (
    repos_education
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST


class CtrEducation(BaseController):
    async def ctr_education(self, ):
        if not self.current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = self.current_user.code

        is_success, education = self.call_repos(
            await repos_education(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(education))
        response_education = dict(
            education_information=None,
            education_level=None,
            professional=None,
            major=None,
            school=None,
            training_method=None,
            ranking=None,
            gpa=None
        )
        if education:
            education_cultural = education['level']['cultural']
            response_education = {
                "education_information": education_cultural['academy'],
                "education_level": education_cultural['education_level'],
                "professional": education_cultural['major'],  # TODO
                "major": education_cultural['major'],  # TODO
                "school": education_cultural['school'],
                "training_method": education_cultural['training'],
                "ranking": education_cultural['degree'],
                "gpa": None  # TODO Điểm tốt nghiệp không tìm thấy
            }

        return self.response(data=response_education)
