from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import (
    repos_get_acc_types, repos_get_withdraw_info, repos_save_withdraw
)
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_WITHDRAW
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.functions import orjson_dumps, orjson_loads


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
                withdraw_account_flag=True,
                withdrawals_amount=beneficiary.withdrawals_amount,
                content=beneficiary.content
            )
        else:
            beneficiary_info = dict(
                withdraw_account_flag=False,
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
                is_transfer_payer=fee.is_transfer_payer,
                payer=fee.payer,
                amount=fee.fee_amount
            ) if fee.is_transfer_payer else None
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

    async def ctr_source_account_info(self, cif_number: str, booking_id: str):
        current_user = self.current_user
        # # Kiểm tra booking
        # await CtrBooking().ctr_get_booking_and_validate(
        #     booking_id=booking_id,
        #     business_type_code=BUSINESS_TYPE_WITHDRAW,
        #     check_correct_booking_flag=False,
        #     loc=f'booking_id: {booking_id}'
        # )

        gw_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_by_cif_number(
            cif_number=cif_number
        )
        account_list = gw_account_info['data']
        account_info_list = account_list['account_info_list']

        response_data = dict(
            total_items=account_list['total_items'],
            casa_accounts=[dict(
                number=account["number"],
            ) for account in account_info_list]
        )
        numbers = []
        for account in response_data['casa_accounts']:
            number = account["number"]
            gw_account_detail = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_info(account_number=number)
            account_detail = gw_account_detail['data']
            customer_info = account_detail['customer_info']
            account_info = account_detail['account_info']
            numbers.append(number)
            account.update(
                number=account_info['number'],
                fullname_vn=customer_info['fullname_vn'],
                balance_available=account_info['balance_available'],
                currency=account_info['currency']
            )
        acc_types = self.call_repos(await repos_get_acc_types(
            numbers=numbers,
            session=self.oracle_session
        ))

        for account in response_data['casa_accounts']:
            number = account["number"]
            for casa_account_number, acc_type in acc_types:
                if number == casa_account_number:
                    account.update(
                        account_type=acc_type
                    )
                    break

        return self.response(response_data)

    async def ctr_withdraw_info(
            self,
            booking_id: str,
    ):
        current_user = self.current_user

        get_pay_in_cash_info = self.call_repos(await repos_get_withdraw_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))

        form_data = orjson_loads(get_pay_in_cash_info.form_data)
        ################################################################################################################
        # Thông tin người thụ hưởng
        ################################################################################################################
        receiver_response = {}
        account_number = form_data['source_accounts']

        gw_casa_account_info = await CtrGWCasaAccount(current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=account_number,
            return_raw_data_flag=True
        )
        gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']
        account_info = gw_casa_account_info_customer_info['account_info']
        receiver_info = form_data['beneficiary_info']

        receiver_response = dict(
            withdraw_account_flag=receiver_info['withdraw_account_flag'],
            currency=account_info['account_currency'],
            withdrawals_amount=receiver_info['withdrawals_amount'],
            content=receiver_info['content']
        )

        ################################################################################################################

        amount = receiver_response['withdrawals_amount']

        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
        fee_info = form_data['fee_info']
        fee_amount = fee_info['amount']
        vat_tax = fee_amount / 10
        total = fee_amount + vat_tax
        actual_total = total + amount
        is_transfer_payer = False
        payer = None
        if fee_info['is_transfer_payer'] is not None:
            payer = "RECEIVER"
            if fee_info['is_transfer_payer'] is True:
                is_transfer_payer = True
                payer = "SENDER"

        fee_info = (dict(
            vat_tax=vat_tax,
            total=total,
            actual_total=actual_total,
            is_transfer_payer=is_transfer_payer,
            payer=payer
        ))

        response_data = dict(
            receiver_response=receiver_response,
            fee_response=fee_info
        )

        return self.response(response_data)
