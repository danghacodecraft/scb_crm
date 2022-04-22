from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.deposit_account.repository import (
    repos_gw_get_deposit_account_by_cif_number, repos_gw_get_deposit_account_td
)


class CtrGWDepositAccount(BaseController):
    async def ctr_gw_get_deposit_account_by_cif_number(
            self,
            cif_number: str
    ):
        current_user = self.current_user
        account_info = self.call_repos(await repos_gw_get_deposit_account_by_cif_number(
            cif_number=cif_number, current_user=current_user))
        response_data = {}
        total_balances = 0
        account_info_list = account_info['selectDepositAccountFromCIF_out']['data_output']['customer_info'][
            'account_info_list']
        account_infos = []
        for account in account_info_list:
            balance = int(account['account_info_item']['account_balance'])
            total_balances += balance
            account_infos.append(account['account_info_item'])

        response_data.update(dict(
            total_balances=total_balances,
            total_items=len(account_infos),
            account_info_list=account_infos
        ))

        return self.response(data=response_data)

    async def ctr_gw_get_deposit_account_td(
            self,
            account_number: str
    ):
        current_user = self.current_user
        response_data = {}
        deposit_account_td = self.call_repos(await repos_gw_get_deposit_account_td(
            account_number=account_number, current_user=current_user))

        customer_info = deposit_account_td['retrieveDepositAccountTD_out']['data_output']['customer_info']

        account_info = customer_info['account_info']

        cif_info = customer_info['cif_info']

        gw_deposit_cif_info_response = dict(
            cif_number=cif_info["cif_num"],
            issued_date=cif_info["cif_issued_date"]
        )

        branch_info = account_info["branch_info"]
        payin_acc = account_info["payin_acc"]
        payout_acc = account_info["payout_acc"]
        staff_info_direct = account_info["staff_info_direct"]
        staff_info_indirect = account_info["staff_info_indirect"]
        gw_deposit_account_info_response = ({
            "number": account_info["account_num"],
            "term": account_info["account_term"],
            "type": account_info["account_type"],
            "type_name": account_info["account_type_name"],
            "saving_serials": account_info["account_saving_serials"],
            "currency": account_info["account_currency"],
            "balance": account_info["account_balance"],
            "available": account_info["account_balance_available"],
            "open_date": account_info["account_open_date"],
            "maturity_date": account_info["account_maturity_date"],
            "lock_status": account_info["account_lock_status"],
            "class_name": account_info["account_class_name"],
            "class_code": account_info["account_class_code"],
            "interest_rate": account_info["account_interest_rate"],
            "branch_info": dict(
                branch_code=branch_info["branch_code"],
                branch_name=branch_info["branch_name"]
            ),
            "payin_acc": dict(
                payin_account=payin_acc["payin_account"]
            ),
            "payout_acc": dict(
                payout_account=payout_acc["payout_account"]
            ),
            "staff_info_direct": dict(
                staff_code=staff_info_direct["staff_code"],
                staff_name=staff_info_direct["staff_name"]
            ),
            "staff_info_indirect": dict(
                staff_code=staff_info_indirect["staff_code"],
                staff_name=staff_info_indirect["staff_name"]
            )
        })

        gw_deposit_customer_info_response = dict(
            fullname_vn=customer_info["full_name"],
            birthday=customer_info["birthday"],
            gender=customer_info["gender"],
            email=customer_info["email"],
            mobile_phone=customer_info["mobile_phone"],
            customer_type=customer_info["customer_type"]
        )

        response_data.update(
            account_info=gw_deposit_account_info_response,
            customer_info=gw_deposit_customer_info_response,
            cif_info=gw_deposit_cif_info_response
        )

        return self.response(data=response_data)
