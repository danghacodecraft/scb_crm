from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.training_in_scb.repository import (
    repos_training_in_scb
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrTrainingInSCB(BaseController):
    async def ctr_training_in_scb(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, training_in_scbs = self.call_repos(
            await repos_training_in_scb(
                employee_id=employee_id
            )
        )
        if not is_success:
            return self.response_exception(msg=str(training_in_scbs))

        response_training_in_scbs = [dict(
            topic=None,
            code=None,
            name=None,
            from_date=None,
            to_date=None,
            result=None
        )]

        if training_in_scbs:

            response_training_in_scbs = []
            for training_in_scb in training_in_scbs:
                topic = training_in_scb["CHU_DE"]
                course_code = training_in_scb["MA_KHOA_HOC"]
                course_name = training_in_scb["TEN_KHOA_HOC"]

                from_date = training_in_scb["TU_NGAY"]
                from_date = datetime_to_date(string_to_datetime(from_date)) if from_date else None

                to_date = training_in_scb["DEN_NGAY"]
                to_date = datetime_to_date(string_to_datetime(to_date)) if to_date else None

                result = training_in_scb["KET_QUA"]

                response_training_in_scbs.append(dict(
                    topic=topic,
                    course_code=course_code,
                    course_name=course_name,
                    from_date=from_date,
                    to_date=to_date,
                    result=result
                ))

        return self.response(data=response_training_in_scbs)
