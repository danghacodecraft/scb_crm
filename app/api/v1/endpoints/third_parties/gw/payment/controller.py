from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_teller_info
)
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_create_booking_payment, repos_gw_payment_amount_block,
    repos_gw_payment_amount_unblock, repos_gw_redeem_account,
    repos_payment_amount_block, repos_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlockRequest, AccountAmountUnblockRequest,
    RedeemAccountRequest
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.fee.controller import CtrAccountFee
from app.api.v1.others.sender.controller import CtrPaymentSender
from app.api.v1.others.statement.controller import CtrStatement
from app.api.v1.others.statement.repository import repos_get_denominations
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_REDEEM_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK, BUSINESS_FORM_AMOUNT_UNBLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import GW_RESPONSE_STATUS_SUCCESS
from app.utils.error_messages import (
    ERROR_ACCOUNT_NUM_EXIST, ERROR_DENOMINATIONS_NOT_EXIST
)
from app.utils.functions import now, orjson_dumps, orjson_loads


class CtrGWPayment(CtrGWCasaAccount, CtrAccountFee):
    async def ctr_get_payment_amount_block(
        self,
        BOOKING_ID: str
    ):
        booking_business_form = await CtrBooking().ctr_get_booking_business_form(booking_id=BOOKING_ID, session=self.oracle_session)
        form_data = orjson_loads(booking_business_form.form_data)
        form_data.update(
            booking_id=BOOKING_ID
        )
        return self.response(data=form_data)

    async def ctr_payment_amount_block(
            self,
            BOOKING_ID: str,
            request: AccountAmountBlockRequest
    ):
        current_user = self.current_user # noqa
        statement = request.fee_payment_info.statement

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )

        denominations__amounts = {}
        statement_info = self.call_repos(await repos_get_denominations(currency_id="VND", session=self.oracle_session))
        management = request.fee_payment_info.management_info
        sender_info = request.fee_payment_info.sender_info

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

        ################################################################################################################
        # Thông tin Tài khoản
        ################################################################################################################
        account_amount_blocks = request.account_amount_blocks
        act_amount_blocks = []
        account_numbers = []
        saving_booking_customer = []  # noqa
        saving_booking_account = []
        cif_number = None
        for item in account_amount_blocks:
            account_numbers.append(item.account_number)
            account_info = await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_casa_account_info(
                account_number=item.account_number,
                return_raw_data_flag=True
            )
            if not account_info:
                return self.response_exception(
                    msg=ERROR_ACCOUNT_NUM_EXIST,
                    loc=str(denominations_errors)
                )
            cif_number = account_info['customer_info']['cif_info']['cif_num']
            act_amount_blocks.append(item.dict())
            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_num": item.account_number,
                "created_at": now()
            })

        if len(set(account_numbers)) != len(account_amount_blocks):
            return self.response_exception(msg="account_number duplicate")

        ################################################################################################################
        # Thông tin Phí
        ################################################################################################################
        fee_info_request = request.fee_payment_info.fee_info
        saving_fee_info = await self.calculate_fees(
            fee_info_request=fee_info_request,
            business_type_id=BUSINESS_TYPE_AMOUNT_BLOCK
        )
        ################################################################################################################
        # Bảng kê tiền giao dịch
        ################################################################################################################
        statement_info = await CtrStatement().ctr_get_statement_info(statement_requests=statement)

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
        management_info = {
            "direct_staff_code": management.direct_staff_code,
            "indirect_staff_code": management.indirect_staff_code,
        },

        request_data = {
            "account_amount_blocks": act_amount_blocks,
            "fee_payment_info": {
                "fee_info": saving_fee_info,
                "statement": statement_info,
                "management_info": management_info,
                "sender_info": sender_response
            },
            "customer_cif_number": cif_number
        }

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
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
            business_type_id=BUSINESS_TYPE_AMOUNT_BLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_data),
            history_datas=orjson_dumps(history_datas),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        booking_id = self.call_repos(await repos_payment_amount_block(
            booking_id=BOOKING_ID,
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
            # saving_booking_customer=saving_booking_customer,
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)

    async def ctr_gw_payment_amount_block(self, BOOKING_ID: str):
        current_user = self.current_user

        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_BLOCK,
                session=self.oracle_session
            ))

        request_data_gw = orjson_loads(booking_business_form.form_data)

        teller = self.call_repos(await repos_get_teller_info(
            booking_id=BOOKING_ID,
            session=self.oracle_session
        ))

        gw_payment_amount_block = self.call_repos(await repos_gw_payment_amount_block(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data_gw,
            teller=teller,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": gw_payment_amount_block
        }

        return self.response(data=response_data)

    async def ctr_payment_amount_unblock(
            self,
            BOOKING_ID: str,
            request: AccountAmountUnblockRequest
    ):
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )

        current_user = self.current_user
        request_data = []
        account_unlock_info = []
        account_numbers = []
        saving_booking_account = []
        statement = request.transaction_fee_info.statement
        management = request.transaction_fee_info.management_info
        sender_info = request.transaction_fee_info.sender_info
        cif_number = None

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

        for item in request.account_unlock:
            if item.account_number in account_numbers:
                return self.response_exception(msg="Duplicate Account_number", detail=f"Account_number {item.account_number}")
            account_unlock_info.append(item.dict())
            account_info = await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_casa_account_info(
                account_number=item.account_number,
                return_raw_data_flag=True
            )
            if not account_info:
                return self.response_exception(
                    msg=ERROR_ACCOUNT_NUM_EXIST,
                    loc=str(denominations_errors)
                )
            cif_number = account_info['customer_info']['cif_info']['cif_num']
            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_num": item.account_number,
                "created_at": now()
            })
            account_numbers.append(item.account_number)

        ################################################################################################################
        # Thông tin Phí
        ################################################################################################################
        fee_info_request = request.transaction_fee_info.fee_info
        saving_fee_info = await self.calculate_fees(
            fee_info_request=fee_info_request,
            business_type_id=BUSINESS_TYPE_AMOUNT_UNBLOCK
        )

        ################################################################################################################
        # Bảng kê tiền giao dịch
        ################################################################################################################
        statement_info = await CtrStatement().ctr_get_statement_info(statement_requests=statement)

        ################################################################################################################
        # Thông tin khách hàng giao dịch
        ################################################################################################################

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

        request_data.append({
            "account_unlock": account_unlock_info,
            "transaction_fee_info": {
                "fee_info": saving_fee_info,
                "statement": statement_info,
                "management_info": {
                    "direct_staff_code": management.direct_staff_code,
                    "indirect_staff_code": management.indirect_staff_code,
                },
                "sender_info": sender_response
            },
            "customer_cif_number": cif_number
        })

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK,
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

        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_data),
            history_datas=orjson_dumps(history_data),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_data

        booking_id = self.call_repos(await repos_payment_amount_unblock(
            booking_id=BOOKING_ID,
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
            # saving_booking_account=saving_booking_account,
            # saving_booking_customer=saving_booking_customer,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)

    async def ctr_gw_payment_amount_unblock(
            self,
            BOOKING_ID: str,
    ):
        current_user = self.current_user
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_UNBLOCK,
                session=self.oracle_session

            ))
        request_data = orjson_loads(booking_business_form.form_data)

        gw_payment_amount_unblock = self.call_repos(await repos_gw_payment_amount_unblock(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
            "account_list": gw_payment_amount_unblock
        }
        return self.response(data=response_data)

    async def ctr_gw_redeem_account(self, redeem_account: RedeemAccountRequest):
        current_user = self.current_user
        payout_details = [{
            "payout_component": item.payout_component,
            "payout_mode": item.payout_mode,
            "payout_amount": item.payout_amount,
            "offset_account": item.offset_account
        } for item in redeem_account.p_payout_detail.payout_details]
        data_input = {
            "account_info": {
                "account_num": redeem_account.account_info.account_number,
            },
            "p_payout_detail": {
                "redemption_details": {
                    "redemption_mode": redeem_account.p_payout_detail.redemption_details.redemption_mode,
                    "redemption_amount": redeem_account.p_payout_detail.redemption_details.redemption_amount,
                    "waive_penalty": redeem_account.p_payout_detail.redemption_details.waive_penalty,
                    "waive_interest": redeem_account.p_payout_detail.redemption_details.waive_interest
                },
                "payout_details": payout_details
            },
            # TODO hard core
            "p_denominated_deposit": "",
            "p_addl_payout_detail": "",
            "p_charges": "",
            "p_denomination": "",
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": ""
                }
            ],
            # TODO hard core
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            # TODO hard core
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        request_data, gw_payment_redeem_account = self.call_repos(
            await repos_gw_redeem_account(
                current_user=current_user,
                data_input=data_input,
            )
        )

        booking_id, booking_code = self.call_repos(await repos_create_booking_payment(
            business_type_code=BUSINESS_TYPE_REDEEM_ACCOUNT,
            current_user=current_user.user_info,
            form_data=request_data,
            log_data=gw_payment_redeem_account,
            session=self.oracle_session
        ))

        redeem_account = gw_payment_redeem_account.get('redeemAccount_out', {})
        # check trường hợp lỗi
        if redeem_account.get('transaction_info').get('transaction_error_code') != GW_RESPONSE_STATUS_SUCCESS:
            return self.response_exception(msg=redeem_account.get('transaction_info').get('transaction_error_msg'))
        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)
