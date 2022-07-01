from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number
)
from app.api.v1.endpoints.deposit.open_deposit.repository import (
    repos_save_td_account
)
from app.utils.functions import generate_uuid, now


class CtrDeposit(BaseController):
    async def ctr_save_deposit_open_td_account(
            self,
            booking_id,
            deposit_account_request
    ):
        current_user = self.current_user
        customer = self.call_repos(
            await repos_get_customer_by_cif_number(
                cif_number=deposit_account_request.cif_number,
                session=self.oracle_session
            )
        )
        td_accounts = []
        td_account_resigns = []
        for item in deposit_account_request.td_account:
            td_account_id = generate_uuid()
            td_accounts.append({
                "id": td_account_id,
                "customer_id": customer.id,
                "currency_id": item.currency_id,
                "account_type_id": item.account_type_id,
                "account_class_id": item.account_class_id,
                "maker_at": now(),
                "maker_id": current_user.user_info.code,
                "checker_id": None,
                "checker_at": None,
                "active_flag": False,
                "amount": item.amount,
                "pay_in_amount": item.pay_in_amount,
                "pay_in_casa_account": item.pay_in_casa_account,
                "pay_out_interest_casa_account": item.pay_out_interest_casa_account,
                "pay_out_casa_account": item.pay_out_casa_account,
                "td_contract_num": item.td_contract_num,
                "fcc_transaction_num": item.fcc_transaction_num,
                "td_resign_type_id": item.td_resign_type_id,
                "maturity_date": item.maturity_date,
                "td_serial": item.td_serial,
                "td_interest_type": item.td_interest_type,
                "td_interest": item.td_interest,
            })
            td_account_resigns.append({
                "id": td_account_id,
                "pay_out_casa_account_resign": item.pay_out_casa_account_resign,
                "td_interest_class_resign": item.td_interest_class_resign,
                "acc_class_id_resign": item.acc_class_id_resign,
                "acc_type_id_resign": item.acc_type_id_resign
            })

        td_account = self.call_repos(await repos_save_td_account(
            td_accounts=td_accounts,
            td_account_resigns=td_account_resigns,
            session=self.oracle_session
        ))

        response_data = td_account

        return self.response(data=response_data)
