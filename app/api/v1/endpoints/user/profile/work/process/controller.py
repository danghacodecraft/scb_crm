from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.process.repository import (
    repos_process_info
)
from app.utils.error_messages import MESSAGE_STATUS, USER_NOT_EXIST
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrProcess(BaseController):
    async def ctr_process_info(self):
        current_user = self.current_user
        if not current_user:
            return self.response_exception(
                msg=USER_NOT_EXIST,
                detail=MESSAGE_STATUS[USER_NOT_EXIST],
                loc="current_user"
            )

        gw_processes = self.call_repos(
            await repos_process_info(
                current_user=current_user
            )
        )

        processes = gw_processes['selectWorkingProcessInfoFromCode_out']['data_output'][
            'working_process_info_list']['working_process_info_item']

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
                    "from_date": datetime_to_date(string_to_datetime(process['from_date'])) if process['from_date'] else None,
                    "to_date": datetime_to_date(string_to_datetime(process['to_date'])) if process['to_date'] else None,
                    "company": process['company'],
                    "position": process['position']
                })

        return self.response_paging(data=response_datas)
