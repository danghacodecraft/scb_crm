import json
from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.others.booking.repository import generate_booking_code
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    TransactionStage, TransactionStageLane, TransactionStagePhase,
    TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.business_type import BUSINESS_TYPE_AMOUNT_UNBLOCK
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK, BUSINESS_FORM_AMOUNT_BLOCK_PD
)
from app.utils.constant.gw import GW_CASA_RESPONSE_STATUS_SUCCESS
from app.utils.error_messages import ERROR_BOOKING_CODE_EXISTED, MESSAGE_STATUS
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
        saving_transaction_stage_lane,
        saving_transaction_stage_phase,
        saving_transaction_stage_role,
        saving_transaction_daily,
        saving_transaction_sender,
        request_json: json,
        history_datas: json,
        session
):
    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        # lưu form data request từ client
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_AMOUNT_BLOCK,
            save_flag=True,
            created_at=now(),
            log_data=history_datas
        ))
    ])

    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )

    return ReposReturn(data=booking_id)


@auto_commit
async def repos_gw_payment_amount_block(
    current_user,
    request_data_gw: list,
    booking_id,
    session: Session
):
    response_data = []
    for item in request_data_gw:
        is_success, gw_payment_amount_block, request_data = await service_gw.gw_payment_amount_block(
            current_user=current_user.user_info, data_input=item
        )

        # lưu form data request GW
        session.add(
            BookingBusinessForm(**dict(
                booking_id=booking_id,
                form_data=orjson_dumps(item),
                business_form_id=BUSINESS_FORM_AMOUNT_BLOCK_PD,
                save_flag=True,
                created_at=now(),
                log_data=orjson_dumps(gw_payment_amount_block)
            ))
        )
        amount_block = gw_payment_amount_block.get('amountBlock_out').get('data_output')

        if isinstance(amount_block, dict):
            response_data.append({
                'account_number': item.get('account_info').get('account_num'),
                'account_ref_no': amount_block.get('account_info').get('blance_lock_info').get('account_ref_no')
            })
        else:
            response_data.append({
                'account_number': item.get('account_info').get('account_num'),
                'account_ref_no': amount_block
            })

    return ReposReturn(data=response_data)


async def repos_gw_payment_amount_unblock(current_user, data_input, session):
    is_success, gw_payment_amount_unblock = await service_gw.gw_payment_amount_unblock(
        data_input=data_input,
        current_user=current_user.user_info
    )

    booking = await repos_create_booking_payment(
        business_type_code=BUSINESS_TYPE_AMOUNT_UNBLOCK,
        current_user=current_user.user_info,
        form_data=data_input,
        log_data=gw_payment_amount_unblock,
        session=session
    )
    booking_id, booking_code = booking.data

    amount_unblock_out = gw_payment_amount_unblock.get('amountUnBlock_out', {})

    # check trường hợp lỗi
    if amount_unblock_out.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=amount_unblock_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=(booking_id, gw_payment_amount_unblock))


async def repos_gw_pay_in_cash(current_user, data_input):
    is_success, gw_pay_in_cash = await service_gw.gw_payment_amount_unblock(
        data_input=data_input,
        current_user=current_user.user_info
    )
    pay_in_cash = gw_pay_in_cash.get('amountUnBlock_out', {})

    # check trường hợp lỗi
    if pay_in_cash.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=pay_in_cash.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_pay_in_cash)


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
