from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.work_profile.repository import (
    repos_work_profile_info
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrWorkProfile(BaseController):
    async def ctr_work_profile_info(self, employee_id: str):

        is_success, work_profile_info = self.call_repos(
            await repos_work_profile_info(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(work_profile_info))

        work_profile_info = work_profile_info['profile']['work']

        working_date = work_profile_info['thu_viec']
        working_date = datetime_to_date(string_to_datetime(working_date)) if working_date else None

        probationary_date = work_profile_info['thu_viec']
        probationary_date = datetime_to_date(string_to_datetime(probationary_date)) if probationary_date else None

        official_date = work_profile_info['thu_viec']
        official_date = datetime_to_date(string_to_datetime(official_date)) if official_date else None

        current_work_profile_info = work_profile_info['cur']
        root_work_profile_info = work_profile_info['org']
        temporary_work_profile_info = work_profile_info['cur']

        work_profile = {
            "working_date": working_date,  # TODO: Ngày làm việc không thấy
            "probationary_date": probationary_date,
            "official_date": official_date,
            "current": {
                "branch": current_work_profile_info['branch_name'],
                "position": current_work_profile_info['job_title_name']
            },
            "root": {
                "branch": root_work_profile_info['branch_name'],
                "position": root_work_profile_info['job_title_name']
            },
            "temporary": {
                "branch": temporary_work_profile_info['branch_name'],
                "position": temporary_work_profile_info['branch_name']
            },
            "seniority_date": probationary_date,
            "is_resident": True  # TODO: Đối tượng cư trú không thấy
        }

        return self.response(data=work_profile)
