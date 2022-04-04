from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.other.training_in_scb.repository import (
    repos_training_in_scb
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrTrainingInSCB(BaseController):
    async def ctr_training_in_scb(self, employee_id: str):
        is_success, training_in_scbs = self.call_repos(
            await repos_training_in_scb(
                employee_id=employee_id
            )
        )
        if not is_success:
            return self.response_exception(msg=str(training_in_scbs))

        return self.response_paging(data=[{
            "topic": training_in_scb["CHU_DE"],
            "course_code": training_in_scb["MA_KHOA_HOC"],
            "course_name": training_in_scb["TEN_KHOA_HOC"],
            "from_date": datetime_to_date(string_to_datetime(training_in_scb["TU_NGAY"]))
            if training_in_scb["TU_NGAY"] else None,
            "to_date": datetime_to_date(string_to_datetime(training_in_scb["DEN_NGAY"]))
            if training_in_scb["DEN_NGAY"] else None,
            "result": training_in_scb["KET_QUA"]
        } for training_in_scb in training_in_scbs])
