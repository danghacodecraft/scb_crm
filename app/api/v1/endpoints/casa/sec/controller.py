from app.api.v1.endpoints.casa.controller import CtrCasa
from app.api.v1.endpoints.casa.sec.repository import repos_save_open_sec_info
from app.api.v1.endpoints.casa.sec.schema import OpenSecRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.fee.controller import CtrAccountFee
from app.api.v1.others.sender.controller import CtrPaymentSender
from app.api.v1.others.statement.controller import CtrStatement
from app.api.v1.validator import validate_history_data
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_SEC
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.error_messages import ERROR_CASA_ACCOUNT_NOT_EXIST
from app.utils.functions import orjson_dumps, orjson_loads


class CtrSecInfo(CtrCasa, CtrBooking, CtrGWCasaAccount, CtrGWCustomer):
    async def ctr_get_open_sec_info(
            self,
            booking_id: str
    ):
        get_open_sec_info = await self.ctr_get_booking_business_form(
            booking_id=booking_id, session=self.oracle_session
        )
        form_data = orjson_loads(get_open_sec_info.form_data)

        return self.response(data=form_data)

    async def ctr_save_open_sec_info(
            self,
            booking_id: str,
            request: OpenSecRequest
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info

        # Kiểm tra booking
        await self.ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_OPEN_SEC,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        # Thông tin Tài khoản
        for account_info in request.account_infos:
            # Kiểm tra số tài khoản có tồn tại hay không
            account_number = account_info.account_number
            casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
                account_number=account_number
            )
            if not casa_account['data']['is_existed']:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                    loc=f"transaction_info -> account_info -> account_number: {account_number}"
                )

        account_info_response = []
        total_sec_amount = 0
        for account_info in request.account_infos:
            sec_amount = account_info.sec_amount
            account_info_response.append(
                dict(
                    account_number=account_info.account_number,
                    sec_amount=sec_amount,
                    sec_unit_amount=sec_amount * 10,
                )
            )
            total_sec_amount += sec_amount

        sender_info = request.transaction_info.sender

        # Lấy thông tin sender, trong controller Casa
        sender_response = await CtrPaymentSender(current_user).get_payment_sender(
            sender_cif_number=sender_info.cif_number,
            sender_full_name_vn=sender_info.full_name_vn,
            sender_address_full=sender_info.address_full,
            sender_identity_number=sender_info.identity_number,
            sender_issued_date=sender_info.issued_date,
            sender_mobile_number=sender_info.mobile_number,
            sender_place_of_issue=sender_info.place_of_issue,
            sender_note=sender_info.full_name_vn
        )

        # Lấy thông tin statement, trong controller Casa
        statement_response = await CtrStatement(current_user).ctr_get_statement_info(
            statement_requests=request.transaction_info.statement)

        # Thông tin phí
        fee_info = request.transaction_info.fee_info
        fee_response = await CtrAccountFee(current_user).calculate_fees(
            fee_info_request=fee_info,
            business_type_id=BUSINESS_TYPE_OPEN_SEC
        )

        response_data = {
            "account_infos": account_info_response,
            "transaction_info": dict(
                content=request.transaction_info.content,
                fee_info=fee_response,
                sender=sender_response,
                statements=statement_response,
                total_sec_amount=total_sec_amount,
                total_sec_unit_amount=total_sec_amount * 10
            ),
            "note": request.note
        }

        if len(fee_response['fee_details']) > 1:
            return self.response_exception(msg='ERROR_INPUT_MORE_THAN_ONE_FEE', loc="fee_response -> fee_details")

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_TOP_UP_CASA_ACCOUNT,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user_info
        )
        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        # Tạo data TransactionDaily và các TransactionStage khác cho bước mở CASA
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_OPEN_SEC,
            booking_id=booking_id,
            request_json=orjson_dumps(response_data),
            history_datas=orjson_dumps(history_datas),
        )

        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        self.call_repos(await repos_save_open_sec_info(
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

        return self.response(data=dict(
            booking_id=booking_id
        ))
