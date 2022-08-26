from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number_optional
)
from app.api.v1.endpoints.deposit.open_deposit.repository import (
    repos_save_pay_in, repos_save_redeem_account, repos_save_td_account
)
from app.api.v1.endpoints.deposit.open_deposit.schema import (
    DepositPayInRequest
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.sender.controller import CtrPaymentSender
from app.api.v1.others.statement.controller import CtrStatement
from app.api.v1.others.statement.repository import repos_get_denominations
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import (
    BUSINESS_TYPE_REDEEM_ACCOUNT, BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_REDEEM_ACCOUNT, BUSINESS_FORM_TD_ACCOUNT_PAY,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_REDEEM_ACCOUNT,
    PROFILE_HISTORY_DESCRIPTIONS_INIT_SAVING_TD_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_DENOMINATIONS_NOT_EXIST
)
from app.utils.functions import generate_uuid, now, orjson_dumps, orjson_loads


class CtrDeposit(BaseController):
    async def ctr_get_deposit_pay_in(self, booking_id: str):
        booking_business_form = self.call_repos(await repos_get_booking_business_form_by_booking_id(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_TD_ACCOUNT_PAY,
            session=self.oracle_session
        ))

        return self.response(data=orjson_loads(booking_business_form.form_data))

    async def ctr_save_deposit_open_td_account(
            self,
            BOOKING_ID,
            deposit_account_request
    ):
        current_user = self.current_user
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )

        is_existed = await CtrGWCustomer(
            current_user=self.current_user).ctr_gw_check_exist_customer_detail_info(
            cif_number=deposit_account_request.cif_number
        )

        if not is_existed:
            return self.response_exception(
                msg=ERROR_CIF_NUMBER_NOT_EXIST, loc=f"open_td_account -> cif_number : {deposit_account_request.cif_number}"
            )
        # lấy thông tin trên crm
        customer = self.call_repos(
            await repos_get_customer_by_cif_number_optional(
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
                "customer_id": customer.id if customer else None,
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
                "pay_in_casa_account": None,
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
                "customer_id": customer.id if customer else None,
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": customer.id if customer else None,
                "cif_number": deposit_account_request.cif_number
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
            business_type_id=BUSINESS_TYPE_TD_ACCOUNT_OPEN_ACCOUNT,
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

    async def ctr_save_deposit_pay_in(self, booking_id: str, deposit_pay_in_request: DepositPayInRequest):
        current_user = self.current_user # noqa

        statement = deposit_pay_in_request.statement
        sender_info = deposit_pay_in_request.sender_info

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
        statement_info = await CtrStatement().ctr_get_statement_info(
            statement_requests=deposit_pay_in_request.statement
        )
        ################################################################################################################
        # Thông tin quản lý
        ################################################################################################################
        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=deposit_pay_in_request.management_info.direct_staff_code,
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=deposit_pay_in_request.management_info.indirect_staff_code,
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )
        mobilization_program = deposit_pay_in_request.management_info.mobilization_program
        management_info_response = dict(
            mobilization_program=mobilization_program,
            direct_staff=direct_staff,
            indirect_staff=indirect_staff
        )
        account_form_response = dict(
            pay_in_form=dict(
                pay_in=deposit_pay_in_request.account_form.pay_in,
                account_number=deposit_pay_in_request.account_form.account_number
            )
        )

        request_data = {
            "account_form": account_form_response,
            "statement_info": statement_info,
            "management_info": management_info_response,
            "sender_info": sender_response
        }

        # Thông tin phí, schema dùng chung, không nên thay đổi chỗ này
        # Response khi gọi ra sẽ dùng để load ra response, nên dùng trong schema response dùng chung trong others.fee
        # fee_info = await CtrAccountFee(current_user=self.current_user).calculate_fees(
        #     fee_info_request=deposit_pay_in_request.fee_info,
        #     business_type_id=BUSINESS_TYPE_REDEEM_OPEN_TD
        # )
        #
        # form_data = deposit_pay_in_request.dict()
        # form_data.update(fee_info=fee_info)

        saving_booking_business_form = dict(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_TD_ACCOUNT_PAY,
            booking_business_form_id=generate_uuid(),
            save_flag=True,
            created_at=now(),
            updated_at=None,
            form_data=orjson_dumps(request_data)
        )

        self.call_repos(await repos_save_pay_in(
            booking_id=booking_id,
            saving_booking_business_form=saving_booking_business_form,
            session=self.oracle_session
        ))
        return self.response(data=dict(
            booking_id=booking_id
        ))

    async def ctr_get_redeem_account_td(self, booking_id):
        booking_business_form = self.call_repos(await repos_get_booking_business_form_by_booking_id(
            booking_id=booking_id,
            business_form_id=BUSINESS_FORM_REDEEM_ACCOUNT,
            session=self.oracle_session
        ))
        response_data = []
        for item in orjson_loads(booking_business_form.form_data):
            response_data.append(orjson_loads(item))
        return self.response(data=response_data)

    async def ctr_save_redeem_account_td(self, booking_id, request):
        current_user = self.current_user
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_REDEEM_ACCOUNT,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )
        requests = []
        for item in request:
            requests.append(item.json())
        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_REDEEM_ACCOUNT,
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
            business_type_id=BUSINESS_TYPE_REDEEM_ACCOUNT,
            booking_id=booking_id,
            request_json=orjson_dumps(requests),
            history_datas=orjson_dumps(history_datas),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        redeem_account_td = self.call_repos(await repos_save_redeem_account( # noqa
            booking_id=booking_id,
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
            session=self.oracle_session
        ))

        return self.response(data=booking_id)
