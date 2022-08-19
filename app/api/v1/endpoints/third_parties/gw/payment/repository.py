from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.repository import generate_booking_code
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer,
    TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_AMOUNT_BLOCK
from app.utils.constant.casa import (
    RECEIVING_METHOD_SCB_BY_IDENTITY, RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK_PD, BUSINESS_FORM_AMOUNT_UNBLOCK_PD
)
from app.utils.constant.gw import (
    GW_FUNC_AMOUNT_BLOCK_OUT, GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_OUT,
    GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_OUT,
    GW_FUNC_INTERBANK_TRANSFER_OUT, GW_FUNC_INTERNAL_TRANSFER_OUT,
    GW_FUNC_TT_LIQUIDATION_OUT, GW_RESPONSE_STATUS_SUCCESS
)
from app.utils.error_messages import (
    ERROR_BOOKING_CODE_EXISTED, ERROR_CALL_SERVICE_GW, MESSAGE_STATUS
)
from app.utils.functions import generate_uuid, now, orjson_dumps


@auto_commit
async def repos_create_booking_payment(
        business_type_code: str,
        current_user,
        session: Session,
        transaction_id: Optional[str] = None,
        form_data: Optional = None,
        log_data: Optional = None
):
    booking_id = generate_uuid()
    current_user_branch_code = current_user.hrm_branch_code
    is_existed, booking_code = await generate_booking_code(
        branch_code=current_user_branch_code,
        business_type_code=business_type_code,
        session=session
    )
    if is_existed:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_CODE_EXISTED + f", booking_code: {booking_code}",
            detail=MESSAGE_STATUS[ERROR_BOOKING_CODE_EXISTED]
        )

    session.add_all([
        Booking(
            id=booking_id,
            # TODO hard core transaction
            transaction_id=None,
            code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            created_at=now(),
            updated_at=now()
        ),
        BookingBusinessForm(
            booking_business_form_id=generate_uuid(),
            booking_id=booking_id,
            business_form_id=business_type_code,
            save_flag=True,
            form_data=orjson_dumps(form_data),
            log_data=orjson_dumps(log_data),
            created_at=now()
        )
    ])
    return ReposReturn(data=(booking_id, booking_code))


@auto_commit
async def repos_payment_amount_block(
        booking_id,
        saving_transaction_stage_status,
        saving_transaction_stage,
        saving_sla_transaction,
        saving_transaction_stage_lane,
        saving_transaction_stage_phase,
        saving_transaction_stage_role,
        saving_transaction_daily,
        saving_transaction_sender,
        saving_transaction_job,
        saving_booking_business_form,
        saving_booking_account,
        saving_booking_customer,
        session
):
    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        SlaTransaction(**saving_sla_transaction),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        # lưu form data request từ client
        BookingBusinessForm(**saving_booking_business_form),
        TransactionJob(**saving_transaction_job)
    ])
    session.bulk_save_objects(BookingAccount(**account) for account in saving_booking_account)
    session.bulk_save_objects(BookingCustomer(**customer) for customer in saving_booking_customer)
    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )

    return ReposReturn(data=booking_id)


async def repos_gw_payment_amount_block(
        current_user,
        request_data_gw,
        booking_id,
        session: Session
):
    for item in request_data_gw.get('account_amount_blocks'):
        data_input = {
            "account_info": {
                "account_num": item['account_number']
            },
            "p_blk_detail": {
                "AMOUNT": item['amount'],
                "AMOUNT_BLOCK_TYPE": item['amount_block_type'],
                "HOLD_CODE": item['hold_code'],
                "EFFECTIVE_DATE": item['effective_date'],
                "EXPIRY_DATE": item['expiry_date'] if item['expiry_date'] else "",
                "REMARKS": item['remarks'],
                "VERIFY_AVAILABLE_BALANCE": item['verify_available_balance'],
                "CHARGE_DETAIL": {
                    "TYPE_CHARGE": "",
                    "ACCOUNT_CHARGE": ""
                }
            },
            # TODO chưa được mô tả
            "p_blk_charge": "",
            # TODO chưa được mô tả
            "p_blk_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": "",
                    "AMOUNT_BLOCK": {
                        "UDF_NAME": "",
                        "UDF_VALUE": ""
                    }
                }
            ],
            "staff_info_checker": {
                # TODO hard core
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                # TODO hard core
                "staff_name": "KHANHLQ"
            }
        }

        is_success, gw_payment_amount_block = await service_gw.gw_payment_amount_block(
            current_user=current_user.user_info, data_input=data_input
        )
        # lưu form data request GW
        saving_booking_business_form = {
            "booking_business_form_id": generate_uuid(),
            "booking_id": booking_id,
            "form_data": orjson_dumps(item),
            "business_form_id": BUSINESS_FORM_AMOUNT_BLOCK_PD,
            "save_flag": True,
            "is_success": True,
            "created_at": now(),
            "out_data": orjson_dumps(gw_payment_amount_block)
        }
        if not is_success:
            saving_booking_business_form.update({
                "is_success": False
            })

        session.add(BookingBusinessForm(**saving_booking_business_form))

        if is_success:
            session.add(TransactionJob(**dict(
                transaction_id=generate_uuid(),
                booking_id=booking_id,
                business_job_id=BUSINESS_JOB_CODE_AMOUNT_BLOCK,
                complete_flag=is_success,
                error_code=gw_payment_amount_block.get(GW_FUNC_AMOUNT_BLOCK_OUT).get('transaction_info').get('transaction_error_code'),
                error_desc=gw_payment_amount_block.get(GW_FUNC_AMOUNT_BLOCK_OUT).get('transaction_info').get('transaction_error_msg'),
                created_at=now()
            )))
        else:
            session.add(TransactionJob(**dict(
                transaction_id=generate_uuid(),
                booking_id=booking_id,
                business_job_id=BUSINESS_JOB_CODE_AMOUNT_BLOCK,
                complete_flag=is_success,
                error_code=None,
                error_desc=None,
                created_at=now()
            )))

        session.commit()
        if not is_success:
            return ReposReturn(
                is_error=True,
                msg=ERROR_CALL_SERVICE_GW,
                loc='PAYMENT_AMOUNT_BLOCK',
                detail=gw_payment_amount_block.get(GW_FUNC_AMOUNT_BLOCK_OUT).get('transaction_info').get('transaction_error_msg')
            )

        # amount_block = gw_payment_amount_block.get(GW_FUNC_AMOUNT_BLOCK_OUT).get('data_output')
        #
        # if isinstance(amount_block, dict):
        #     response_data.append({
        #         'account_number': item.get('account_info').get('account_num'),
        #         'account_ref_no': amount_block.get('account_info').get('blance_lock_info').get('account_ref_no')
        #     })
        # else:
        #     response_data.append({
        #         'account_number': item.get('account_info').get('account_num'),
        #         'account_ref_no': amount_block
        #     })

    return ReposReturn(data=booking_id)


@auto_commit
async def repos_payment_amount_unblock(
        booking_id: str,
        saving_transaction_stage_status: dict,
        saving_sla_transaction: dict,
        saving_transaction_stage: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        saving_transaction_job: dict,
        saving_booking_business_form: dict,
        saving_booking_customer,
        saving_booking_account,
        session
):
    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        SlaTransaction(**saving_sla_transaction),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        # lưu form data request từ client
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)
    ])
    session.bulk_save_objects(BookingAccount(**account) for account in saving_booking_account)
    session.bulk_save_objects(BookingCustomer(**customer) for customer in saving_booking_customer)
    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )
    return ReposReturn(data=booking_id)


@auto_commit
async def repos_gw_payment_amount_unblock(
        current_user,
        request_data_gw: list,
        booking_id,
        session
):
    response_data = []
    for item in request_data_gw.account_unlock:
        is_success, gw_payment_amount_unblock = await service_gw.gw_payment_amount_unblock(
            data_input=item,
            current_user=current_user.user_info
        )

        # lưu form data request GW
        session.add(
            BookingBusinessForm(**dict(
                booking_business_form_id=generate_uuid(),
                booking_id=booking_id,
                form_data=orjson_dumps(item),
                business_form_id=BUSINESS_FORM_AMOUNT_UNBLOCK_PD,
                save_flag=True,
                created_at=now(),
                log_data=orjson_dumps(gw_payment_amount_unblock)
            ))
        )
        amount_unblock = gw_payment_amount_unblock.get('amountUnBlock_out').get('transaction_info')

        response_data.append({
            "account_ref": item.get('account_info').get('balance_lock_info').get('account_ref_no'),
            "transaction": {
                "code": amount_unblock.get('transaction_error_code'),
                "msg": amount_unblock.get('transaction_error_msg')
            }
        })

    return ReposReturn(data=response_data)


async def repos_gw_redeem_account(current_user, data_input):
    request_data = service_gw.gw_create_request_body(
        current_user=current_user.user_info,
        function_name="redeemAccount_in",
        data_input=data_input
    )
    is_success, gw_payment_redeem_account = await service_gw.gw_payment_redeem_account(
        request_data=request_data
    )

    return ReposReturn(data=(request_data, gw_payment_redeem_account))


async def repos_gw_pay_in_cash(
        current_user: AuthResponse, data_input: dict
):
    gw_pay_in_cash = await service_gw.gw_pay_in_cash(
        data_input=data_input,
        current_user=current_user.user_info
    )

    return ReposReturn(data=gw_pay_in_cash)


async def repos_gw_tele_transfer(
    current_user: AuthResponse, data_input: dict
):
    gw_tele_transfer = await service_gw.gw_tele_transfer(
        data_input=data_input,
        current_user=current_user.user_info
    )
    return ReposReturn(data=gw_tele_transfer)


async def repos_gw_tt_liquidation(
    current_user: AuthResponse, data_input: dict
):
    gw_tt_liquidation = await service_gw.gw_payment_tt_liquidation(
        data_input=data_input,
        current_user=current_user.user_info
    )
    return ReposReturn(data=gw_tt_liquidation)


async def repos_gw_interbank_transfer(
        current_user: AuthResponse, data_input: dict
):
    gw_interbank_transfer = await service_gw.gw_interbank_transfer(
        data_input=data_input,
        current_user=current_user.user_info
    )

    return ReposReturn(data=gw_interbank_transfer)


async def repos_pay_in_cash_247_by_acc_num(
        current_user: AuthResponse, data_input: dict
):
    gw_pay_in_cash_247_by_acc_num = await service_gw.gw_pay_in_cash_247_by_acc_num(
        data_input=data_input,
        current_user=current_user.user_info
    )

    return ReposReturn(data=gw_pay_in_cash_247_by_acc_num)


async def repos_pay_in_cash_247_by_card_num(
        current_user: AuthResponse, data_input: dict
):
    gw_pay_in_cash_247_by_card_num = await service_gw.gw_pay_in_cash_247_by_card_num(
        data_input=data_input,
        current_user=current_user.user_info
    )

    return ReposReturn(data=gw_pay_in_cash_247_by_card_num)


async def repos_gw_save_casa_transfer_info(
        current_user,
        receiving_method: str,
        request_data,
        booking_id
):
    gw_casa_transfer, function_out, is_success = None, None, False
    if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_internal_transfer(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='gw_payment_internal_transfer')
        function_out = GW_FUNC_INTERNAL_TRANSFER_OUT

    if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
        is_success, gw_casa_transfer = await service_gw.gw_payment_tt_liquidation(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='repos_gw_save_casa_transfer_info')
        function_out = GW_FUNC_TT_LIQUIDATION_OUT

    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='repos_gw_save_casa_transfer_info')
        function_out = GW_FUNC_INTERBANK_TRANSFER_OUT

    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
        is_success, gw_casa_transfer = await service_gw.gw_interbank_transfer(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='repos_gw_save_casa_transfer_info')
        function_out = GW_FUNC_INTERBANK_TRANSFER_OUT

    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer_247_by_account_number(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='repos_gw_save_casa_transfer_info')
        function_out = GW_FUNC_INTERBANK_TRANSFER_247_BY_ACC_NUM_OUT

    if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
        is_success, gw_casa_transfer = await service_gw.gw_payment_interbank_transfer_247_by_card_number(
            current_user=current_user.user_info, data_input=request_data["data_input"]
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_GW,
                               detail=str(gw_casa_transfer), loc='repos_gw_save_casa_transfer_info')
        function_out = GW_FUNC_INTERBANK_TRANSFER_247_BY_CARD_NUM_OUT

    if not gw_casa_transfer:
        return ReposReturn(is_error=True, msg="No GW Casa Transfer")

    casa_transfer = gw_casa_transfer.get(function_out, {})

    # check trường hợp lỗi
    if casa_transfer.get('transaction_info').get('transaction_error_code') != GW_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=casa_transfer.get('transaction_info').get('transaction_error_msg'))

    response_data = {
        "booking_id": booking_id,
        "p_contract_ref": casa_transfer['data_output']['p_contract_ref']
        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY else None
    }

    return ReposReturn(data=(response_data, gw_casa_transfer, is_success))
