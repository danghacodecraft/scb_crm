from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import (
    repos_get_acc_types, repos_get_withdraw_info, repos_save_withdraw
)
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.sender.controller import CtrPaymentSender
from app.api.v1.others.statement.controller import CtrStatement
from app.api.v1.others.statement.repository import repos_get_denominations
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_WITHDRAW
from app.utils.constant.cif import (
    CHECK_CONDITION_VAT, CHECK_CONDITION_WITHDRAW,
    PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.error_messages import (
    ERROR_AMOUNT_INVALID, ERROR_CASA_ACCOUNT_NOT_EXIST,
    ERROR_CASA_BALANCE_UNAVAILABLE, ERROR_DENOMINATIONS_NOT_EXIST
)
from app.utils.functions import orjson_dumps, orjson_loads


class CtrWithdraw(BaseController):

    async def ctr_save_withdraw_info(
            self,
            booking_id: str,
            request: WithdrawRequest
    ):
        current_user = self.current_user
        statement = request.customer_info.statement
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_WITHDRAW,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_WITHDRAW}"
        )

        denominations__amounts = {}
        statement_info = self.call_repos(await repos_get_denominations(currency_id="VND", session=self.oracle_session))

        for item in statement_info:
            denominations__amounts.update({
                str(int(item.denominations)): 0
            })
        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in denominations__amounts:
                denominations_errors.append(dict(
                    index=index,
                    value=denominations
                ))

            denominations__amounts[denominations] = row.amount

        if denominations_errors:
            return self.response_exception(
                msg=ERROR_DENOMINATIONS_NOT_EXIST,
                loc=str(denominations_errors)
            )

        casa_account_number = request.transaction_info.source_accounts.account_num
        if request.transaction_info.receiver_info.amount < CHECK_CONDITION_WITHDRAW:
            return self.response_exception(
                msg=ERROR_AMOUNT_INVALID,
                loc=f"amount: {request.transaction_info.receiver_info.amount}"
            )

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=casa_account_number
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"account_number: {casa_account_number}"
            )
        receiver = request.transaction_info.receiver_info
        account = request.transaction_info.source_accounts
        sender_info = request.customer_info.sender_info

        # Thông tin khách hàng giao dịch
        sender_response = await CtrPaymentSender(self.current_user).get_payment_sender(
            sender_cif_number=sender_info.cif_number,
            sender_full_name_vn=sender_info.fullname_vn,
            sender_address_full=sender_info.address_full,
            sender_identity_number=sender_info.identity,
            sender_issued_date=sender_info.issued_date,
            sender_mobile_number=sender_info.mobile_phone,
            sender_place_of_issue=sender_info.place_of_issue,
            sender_note=sender_info.note
        )

        statement_info = await CtrStatement().ctr_get_statement_info(statement_requests=request.customer_info.statement)
        amount = request.transaction_info.receiver_info.amount
        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
        fee_info_response = {}
        is_transfer_payer = request.transaction_info.fee_info.is_transfer_payer
        if is_transfer_payer:
            payer_flag = request.transaction_info.fee_info.payer_flag
            fee_info = request.transaction_info.fee_info
            fee_amount = fee_info.amount
            note = request.transaction_info.fee_info.note
            if payer_flag:
                vat_tax = fee_amount / CHECK_CONDITION_VAT
                total = fee_amount + vat_tax
                actual_total = total + amount
                fee_info_response.update(dict(
                    fee_amount=fee_info.amount,
                    vat_tax=vat_tax,
                    total=total,
                    actual_total=actual_total,
                    is_transfer_payer=is_transfer_payer,
                    payer_flag=payer_flag,
                    note=note
                ))
            else:
                vat_tax = fee_amount / 10
                total = fee_amount + vat_tax
                is_transfer_payer = False
                fee_info_response.update(dict(
                    fee_amount=fee_info.amount,
                    vat_tax=vat_tax,
                    total=total,
                    actual_total=amount,
                    is_transfer_payer=is_transfer_payer,
                    payer_flag=payer_flag,
                    note=note
                ))
        else:
            fee_info_response.update(dict(
                is_transfer_payer=is_transfer_payer
            ))

        ################################################################################################################
        # Thông tin quản lý
        ################################################################################################################
        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=request.customer_info.management_info.direct_staff_code,
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=request.customer_info.management_info.indirect_staff_code,
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )
        management_info_response = dict(
            direct_staff=direct_staff,
            indirect_staff=indirect_staff
        )

        data_input = {
            "transaction_info": {
                "source_accounts": {
                    "account_num": account.account_num
                },
                "receiver_info": {
                    "withdraw_account_flag": receiver.withdraw_account_flag,
                    "currency": receiver.currency,
                    "amount": receiver.amount,
                    "content": receiver.content,
                },
                "fee_info": fee_info_response
            },
            "customer_info": {
                "statement_info": statement_info,
                "management_info": management_info_response,
                "sender_info": sender_response
            }
        }
        # Kiểm tra số tiền rút có đủ hay không
        casa_account_balance = await CtrGWCasaAccount(current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=casa_account_number,
            return_raw_data_flag=True
        )
        balance = casa_account_balance['customer_info']['account_info']['account_balance']
        if int(balance) - receiver.amount < CHECK_CONDITION_WITHDRAW:
            return self.response_exception(
                msg=ERROR_CASA_BALANCE_UNAVAILABLE,
                loc=f"account_balance: {balance}"
            )

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_WITHDRAW,
            booking_id=booking_id,
            request_json=orjson_dumps(data_input),
            history_datas=orjson_dumps(history_data)
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_data

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
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)

    async def ctr_source_account_info(self, cif_number: str, booking_id: str):
        current_user = self.current_user
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_WITHDRAW,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

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
                full_name_vn=customer_info['fullname_vn'],
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
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_WITHDRAW,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        get_pay_in_cash_info = self.call_repos(await repos_get_withdraw_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))

        form_data = orjson_loads(get_pay_in_cash_info.form_data)
        ################################################################################################################
        account_number = form_data['transaction_info']['source_accounts']['account_num']
        receiver_response = form_data['transaction_info']['receiver_info']
        fee_info_response = form_data['transaction_info']['fee_info']
        statement_info = form_data['customer_info']['statement_info']
        management_info = form_data['customer_info']['management_info']
        sender_info = form_data['customer_info']['sender_info']

        response_data = dict(
            casa_account=dict(
                account_number=account_number
            ),
            transaction_response=dict(
                receiver_info_response=receiver_response,
                fee_info_response=fee_info_response
            ),
            transactional_customer_response=dict(
                statement_info_response=statement_info,
                management_info_response=management_info,
                sender_info_response=sender_info
            )
        )

        return self.response(response_data)
