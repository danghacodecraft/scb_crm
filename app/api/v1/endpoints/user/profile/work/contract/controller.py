from app.api.base.controller import BaseController
from app.api.v1.endpoints.user.profile.work.contract.repository import (
    repos_contract
)
from app.utils.functions import datetime_to_date, string_to_datetime


class CtrContract(BaseController):
    async def ctr_contract_info(self, employee_id: str):

        is_success, contract_info = self.call_repos(
            await repos_contract(
                employee_id=employee_id,
                session=self.oracle_session
            )
        )
        if not is_success:
            self.response_exception(msg=str(contract_info))

        contract_info = contract_info['profile']['contract']

        start_date = contract_info['start_date']
        start_date = datetime_to_date(string_to_datetime(start_date)) if start_date else None

        end_date = contract_info['start_date']
        end_date = datetime_to_date(string_to_datetime(end_date)) if end_date else None

        contract = {
            "type": contract_info['type'],
            "number": contract_info['name'],
            "start_date": start_date,
            "end_date": end_date,
            "addendum": {
                "number": None,  # TODO: Số phụ lục hợp đồng không thấy
                "start_date": None,   # TODO: ngày bắt đầu không thấy
                "end_date": None,  # TODO: Ngày kết thúc không thấy
            },
            "resign_date": end_date
        }

        return self.response(data=contract)
