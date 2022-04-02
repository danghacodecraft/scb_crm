from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.decisive_contract.repository import (
    repos_decisive_contract
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrDecisiveContract(BaseController):
    async def ctr_decisive_contract(self, employee_id: str):

        is_success, decisive_contract = self.call_repos(
            await repos_decisive_contract(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            self.response_exception(msg=str(decisive_contract))

        start_date = decisive_contract['profile']['contract']['start_date']
        start_date = datetime_to_date(string_to_datetime(start_date)) if start_date else None

        end_date = decisive_contract['profile']['contract']['start_date']
        end_date = datetime_to_date(string_to_datetime(end_date)) if end_date else None

        decisive_contract = {
            "type": decisive_contract['profile']['contract']['type'],
            "number": decisive_contract['profile']['contract']['name'],
            "start_date": start_date,
            "end_date": end_date,
            "addendum": {
                "number": None,  # TODO: Số phụ lục hợp đồng không thấy
                "start_date": None,   # TODO: ngày bắt đầu không thấy
                "end_date": None,  # TODO: Ngày kết thúc không thấy
            },
            "resign_date": end_date
        }

        return self.response(data=decisive_contract)
