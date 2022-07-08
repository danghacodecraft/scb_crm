from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number
)
from app.api.v1.endpoints.deposit.open_deposit.repository import (
    repos_save_td_account, repos_update_td_account
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.repository import (
    repos_get_booking_account_by_booking
)
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_TD_ACCOUNT
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import generate_uuid, now, orjson_dumps


class CtrDeposit(BaseController):
    async def ctr_save_deposit_open_td_account(
            self,
            BOOKING_ID,
            deposit_account_request
    ):
        current_user = self.current_user
        customer = self.call_repos(
            await repos_get_customer_by_cif_number(
                cif_number=deposit_account_request.cif_number,
                session=self.oracle_session
            )
        )
        td_account_ids = []
        td_accounts = []
        td_account_resigns = []
        for item in deposit_account_request.td_account:
            td_account_id = generate_uuid()
            td_account_ids.append(td_account_id)
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
                "maturity_date": item.maturity_date,
                "td_serial": item.td_serial,
                "td_interest_type": item.td_interest_type,
                "td_interest": item.td_interest,
                "td_rollover_type": item.td_rollover_type
            })
            td_account_resigns.append({
                "id": td_account_id,
                "pay_out_casa_account_resign": item.pay_out_casa_account_resign,
                "td_interest_class_resign": item.td_interest_class_resign,
                "acc_class_id_resign": item.acc_class_id_resign,
                "acc_type_id_resign": item.acc_type_id_resign
            })

        saving_booking_account = []
        saving_booking_customer = []
        for account_id in td_account_ids:
            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "td_account_id": account_id,
                "customer_id": customer.id,
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": customer.id
            })

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        # Tạo data TransactionDaily và các TransactionStage
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_OPEN_TD_ACCOUNT,
            booking_id=BOOKING_ID,
            request_json=deposit_account_request.json(),
            history_datas=orjson_dumps(history_datas),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        booking_id = self.call_repos(await repos_save_td_account(
            booking_id=BOOKING_ID,
            td_accounts=td_accounts,
            td_account_resigns=td_account_resigns,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)

    async def ctr_save_deposit_pay_in(self, BOOKING_ID, deposit_pay_in_request):
        booking_accounts = self.call_repos(await repos_get_booking_account_by_booking(
            booking_id=BOOKING_ID,
            session=self.oracle_session
        ))
        update_td_account = []
        for item in booking_accounts:
            update_td_account.append({
                "id": item.id,
                "pay_in_casa_account": deposit_pay_in_request.account_form.pay_in_form.account_number,
                "pay_in_type": deposit_pay_in_request.account_form.pay_in_form.pay_in,
            })
        booking_id = self.call_repos(await repos_update_td_account(
            BOOKING_ID,
            update_td_account=update_td_account,
            session=self.oracle_session
        ))
        return self.response(data=booking_id)
