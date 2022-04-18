from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.process.repository import (
    repos_process_info
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrProcess(BaseController):
    async def ctr_process_info(self):
        current_user = self.current_user.user_info
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        employee_id = current_user.code

        is_success, processes = self.call_repos(
            await repos_process_info(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            return self.response_exception(msg=str(processes))

        response_datas = [dict(
            from_date=None,
            to_date=None,
            company=None,
            position=None
        )]
        if processes:
            response_datas = []
            for process in processes:
                response_datas.append({
                    "from_date": datetime_to_date(string_to_datetime(process['TU_NGAY'])) if process['TU_NGAY'] else None,
                    "to_date": datetime_to_date(string_to_datetime(process['DEN_NGAY'])) if process['DEN_NGAY'] else None,
                    "company": process['CONG_TY'],
                    "position": process['CHUC_VU']
                })

        return self.response_paging(data=response_datas)
