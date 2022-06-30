from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import repos_save_withdraw
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_WITHDRAW
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import orjson_dumps


class CtrWithdraw(BaseController):

    async def ctr_save_withdraw_info(
            self,
            booking_id: str,
            request: WithdrawRequest
    ):
        current_user = self.current_user
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_WITHDRAW,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_WITHDRAW}"
        )

        beneficiary = request.transaction_information.beneficiary_information
        fee = request.transaction_information.fee_information
        if beneficiary.withdraw_account_flag:
            beneficiary_info = dict(
                withdrawals_amount=beneficiary.withdrawals_amount,
                content=beneficiary.content
            )
        else:
            beneficiary_info = dict(
                withdrawals_amount=beneficiary.withdrawals_amount,
                seri_cheque=beneficiary.seri_cheque,
                date_of_issue=beneficiary.date_of_issue,
                exchange_VND_flag=beneficiary.exchange_VND_flag,
                exchange_rate=beneficiary.exchange_rate,
                exchanged_money_VND=beneficiary.exchanged_money_VND,
                reciprocal_rate_headquarters=beneficiary.reciprocal_rate_headquarters,
                content=beneficiary.content
            )

        transaction_info = dict(
            source_accounts=request.transaction_information.source_accounts.account_num,
            beneficiary_info=beneficiary_info,
            fee_info=dict(
                charge_name=fee.charge_name,
                charge_amount=fee.charge_amount
            ) if fee.waived else None
        )

        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init_cif(
            business_type_id=BUSINESS_TYPE_WITHDRAW
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender
        ) = transaction_data

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_data)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        booking_id = self.call_repos(await repos_save_withdraw(
            booking_id=booking_id,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            request_json=orjson_dumps(transaction_info),
            history_data=orjson_dumps(history_data),
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)
