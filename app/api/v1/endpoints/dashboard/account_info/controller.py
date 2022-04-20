from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.account_info.repository import (
    get_deposit_account_by_cif_number
)
from app.api.v1.endpoints.third_parties.repository import (
    repos_gw_get_casa_account_by_cif_number
)


class CtrAccountInfo(BaseController):
    async def ctr_get_account_info(
            self,
            cif_number: str
    ):
        account_info = self.call_repos(await repos_gw_get_casa_account_by_cif_number(cif_number=cif_number))
        response_data = {}
        total_balances = 0
        account_info_list = account_info['selectCurrentAccountFromCIF_out']['data_output']['customer_info'][
            'account_info_list']
        account_infos = []
        for account in account_info_list:
            balance = int(account['account_info_item']['account_balance'])
            total_balances += balance
            account_infos.append(account['account_info_item'])

        response_data.update({"payment_account": dict(
            total_balances=total_balances,
            total_items=len(account_infos),
            account_info_list=account_infos)}
        )

        deposit_info = self.call_repos(await get_deposit_account_by_cif_number(cif_number=cif_number))
        total_balances = 0
        deposit_info_list = deposit_info['selectDepositAccountFromCIF_out']['data_output']['customer_info'][
            'account_info_list']
        deposit_infos = []
        for account in deposit_info_list:
            balance = int(account['account_info_item']['account_balance'])
            total_balances += balance
            deposit_infos.append(account['account_info_item'])

        response_data.update(
            {
                "deposit_account": dict(
                    total_balances=total_balances,
                    total_items=len(account_infos),
                    account_info_list=account_infos),
                "loan_account": None,
                "credit_card": None,
                "atm_debit_card": None
            }
        )

        response_data.update({

        })

        return self.response(data=response_data)
