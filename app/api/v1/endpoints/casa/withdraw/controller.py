from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import (
    repos_get_acc_types, repos_get_withdraw_info, repos_save_withdraw
)
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_WITHDRAW
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_WITHDRAW, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.error_messages import ERROR_CASA_ACCOUNT_NOT_EXIST
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

        casa_account_number = request.transaction_info.source_accounts.account_num

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
        fee = request.transaction_info.fee_info
        management = request.customer_info.management_info
        transactional_customer = request.customer_info.sender_info
        if receiver.withdraw_account_flag:
            receiver_info = dict(
                withdraw_account_flag=True,
                amount=receiver.amount,
                content=receiver.content
            )
        else:
            receiver_info = dict(
                withdraw_account_flag=False,
                amount=receiver.amount,
                seri_cheque=receiver.seri_cheque,
                date_of_issue=receiver.date_of_issue,
                exchange_VND_flag=receiver.exchange_VND_flag,
                exchange_rate=receiver.exchange_rate,
                exchanged_money_VND=receiver.exchanged_money_VND,
                reciprocal_rate_headquarters=receiver.reciprocal_rate_headquarters,
                content=receiver.content
            )

        transaction_info = dict(
            source_accounts=request.transaction_info.source_accounts.account_num,
            receiver_info=receiver_info,
            fee_info=dict(
                is_transfer_payer=fee.is_transfer_payer,
                payer=fee.payer,
                amount=fee.fee_amount
            ) if fee.is_transfer_payer else None
        )

        transactional_customer_info = dict(
            management_info=dict(
                direct_staff_code=management.direct_staff_code,
                indirect_staff_code=management.indirect_staff_code
            ),
            sender_info=dict(
                cif_flag=transactional_customer.cif_flag,
                cif_number=transactional_customer.cif_number,
                note=transactional_customer.note
            ) if transactional_customer.cif_flag else dict(
                cif_flag=transactional_customer.cif_flag,
                fullname_vn=transactional_customer.fullname_vn,
                identity=transactional_customer.identity,
                issued_date=transactional_customer.issued_date,
                place_of_issue=transactional_customer.place_of_issue,
                address_full=transactional_customer.address_full,
                mobile_phone=transactional_customer.mobile_phone,
                note=transactional_customer.note,
            )
        )

        data_request = dict(
            transaction_info=transaction_info,
            transactional_customer_info=transactional_customer_info
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
            request_json=orjson_dumps(data_request),
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
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_WITHDRAW,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )
        current_user = self.current_user

        get_pay_in_cash_info = self.call_repos(await repos_get_withdraw_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))

        form_data = orjson_loads(get_pay_in_cash_info.form_data)
        ################################################################################################################
        # Thông tin người thụ hưởng
        ################################################################################################################
        account_number = form_data['transaction_info']['source_accounts']

        gw_casa_account_info = await CtrGWCasaAccount(current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=account_number,
            return_raw_data_flag=True
        )
        gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']
        account_info = gw_casa_account_info_customer_info['account_info']
        receiver_info = form_data['transaction_info']['receiver_info']

        receiver_response = dict(
            withdraw_account_flag=receiver_info['withdraw_account_flag'],
            currency=account_info['account_currency'],
            amount=receiver_info['amount'],
            content=receiver_info['content']
        )

        ################################################################################################################
        amount = receiver_response['amount']

        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
        fee_info = form_data['transaction_info']['fee_info']
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

        fee_info_response = (dict(
            fee_amount=fee_info['amount'],
            vat_tax=vat_tax,
            total=total,
            actual_total=actual_total,
            is_transfer_payer=is_transfer_payer,
            payer=payer
        ))

        ################################################################################################################
        # Thông tin quản lý
        ################################################################################################################
        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['transactional_customer_info']['management_info']['direct_staff_code'],
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['transactional_customer_info']['management_info']['indirect_staff_code'],
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )

        ################################################################################################################
        # Thông tin khách hàng giao dịch
        ################################################################################################################
        cif_flag = form_data['transactional_customer_info']['sender_info']['cif_flag']
        sender_response = {}
        customer_info = form_data['transactional_customer_info']['sender_info']

        if cif_flag:
            cif_number = form_data['transactional_customer_info']['sender_info']['cif_number']
            gw_customer_info = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
                cif_number=cif_number,
                return_raw_data_flag=True
            )
            gw_customer_info_identity_info = gw_customer_info['id_info']
            gw_customer_info_address_info = gw_customer_info['p_address_info']
            sender_response.update(
                cif_flag=cif_flag,
                cif_number=cif_number,
                fullname_vn=gw_customer_info['full_name'],
                address_full=gw_customer_info_address_info['address_full'],
                identity=gw_customer_info_identity_info['id_num'],
                issued_date=gw_customer_info_identity_info['id_issued_date'],
                place_of_issue=gw_customer_info_identity_info['id_issued_location'],
                mobile_phone=gw_customer_info['mobile_phone'],
                note=customer_info['note']
            )
        else:
            sender_response.update(
                cif_flag=cif_flag,
                fullname_vn=customer_info['fullname_vn'],
                address_full=customer_info['address_full'],
                identity=customer_info['identity'],
                issued_date=customer_info['issued_date'],
                place_of_issue=customer_info['place_of_issue'],
                mobile_phone=customer_info['mobile_phone'],
                note=customer_info['note']
            )

        response_data = dict(
            transaction_response=dict(
                receiver_info_response=receiver_response,
                fee_info_response=fee_info_response
            ),
            transactional_customer_response=dict(
                management_info_response=dict(
                    direct_staff=direct_staff,
                    indirect_staff=indirect_staff
                ),
                sender_info_response=sender_response
            )
        )

        return self.response(response_data)
