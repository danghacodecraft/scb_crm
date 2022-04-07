from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.work_profile.repository import (
    repos_work_profile_info
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrWorkProfile(BaseController):
    async def ctr_work_profile_info(self):
        if not self.current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = self.current_user.user_info.code

        is_success, work_profile_info = self.call_repos(
            await repos_work_profile_info(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(work_profile_info))

        response_foreign = dict(
            avatar=None,
            working_date=None,
            probationary_date=None,
            official_date=None,
            current=None,
            root=None,
            temporary=None,
            seniority_date=None,
            is_resident=None
        )
        response_foreign["current"] = dict(
            branch=None,
            position=None
        )
        response_foreign["root"] = dict(
            branch=None,
            position=None
        )
        response_foreign["temporary"] = dict(
            branch=None,
            position=None
        )

        if work_profile_info:
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

            response_foreign = {
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

        return self.response(data=response_foreign)
