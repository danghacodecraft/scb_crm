from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.deposit.repository import (
    repos_get_acc_class, repos_get_acc_type, repos_get_account_detail,
    repos_get_interest_type_by_id, repos_get_serial
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.cif.e_banking.model import TdInterestType
from app.third_parties.oracle.models.master_data.deposit import TDRolloverType
from app.utils.functions import dropdown_name


class CtrConfigDeposit(BaseController):
    async def ctr_get_rollover_type(self):
        rollover_type = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=TDRolloverType
            )
        )

        return self.response(data=rollover_type)

    async def ctr_get_interest_type(self):
        interest_type = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=TdInterestType
            )
        )

        return self.response(data=interest_type)

    async def ctr_get_acc_type(self):
        current = self.current_user

        acc_type = self.call_repos(
            await repos_get_acc_type(
                current_user=current.user_info
            )
        )
        response_data = []

        for item in acc_type:
            response_data.append(dropdown_name(name=item['SAN_PHAM_CAP_3']))

        return self.response(data=response_data)

    async def ctr_get_acc_class(self, acc_class_request):
        current = self.current_user

        interest = self.call_repos(
            await repos_get_interest_type_by_id(
                interest_type_id=acc_class_request.interest_type_id,
                session=self.oracle_session
            )
        )

        acc_class = self.call_repos(
            await repos_get_acc_class(
                current_user=current.user_info,
                interest=interest,
                acc_type=acc_class_request.acc_type,
                currency_id=acc_class_request.currency_id
            )
        )

        return self.response(data=acc_class)

    async def ctr_get_serial(self, serial_request):
        current = self.current_user
        account_class = serial_request.account_class
        account_detail = self.call_repos(
            await repos_get_account_detail(
                account_class=account_class,
                current_user=current.user_info
            )
        )
        serial = self.call_repos(
            await repos_get_serial(
                serial_prefix=account_detail['MAKYHIEU'],
                serial_key=account_detail['MAANCHI'],
                current_user=current.user_info
            )
        )
        return self.response(data=serial)
