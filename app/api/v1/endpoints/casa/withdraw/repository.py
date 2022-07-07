from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_WITHDRAW
from app.utils.constant.cif import BUSINESS_FORM_WITHDRAW_PD
from app.utils.error_messages import ERROR_BOOKING_ID_NOT_EXIST
from app.utils.functions import generate_uuid, now, orjson_dumps


@auto_commit
async def repos_save_withdraw(
        booking_id: str,
        saving_transaction_stage_status: dict,
        saving_transaction_stage: dict,
        saving_transaction_stage_lane: dict,
        saving_sla_transaction: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        saving_transaction_job: dict,
        saving_booking_business_form: dict,
        session: Session
) -> ReposReturn:
    # Lưu log vào DB
    session.add_all([
        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSINESS_FORM
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        SlaTransaction(**saving_sla_transaction),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)
    ])
    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )
    session.flush()

    return ReposReturn(data=booking_id)


@auto_commit
async def repos_gw_withdraw(
        current_user,
        request_data_gw,
        booking_id,
        session: Session
):
    response_data = []
    is_success, gw_withdraw, request_data = await service_gw.gw_withdraw(
        current_user=current_user.user_info, data_input=request_data_gw
    )

    # lưu form data request GW
    session.add(
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=orjson_dumps(request_data_gw),
            business_form_id=BUSINESS_FORM_WITHDRAW_PD,
            save_flag=True,
            created_at=now(),
            log_data=orjson_dumps(gw_withdraw)
        ))
    )

    session.add(TransactionJob(**dict(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_WITHDRAW,
        complete_flag=is_success,
        error_code=gw_withdraw.get('cashWithdrawals_out').get('transaction_info').get(
            'transaction_error_code'),
        error_desc=gw_withdraw.get('cashWithdrawals_out').get('transaction_info').get(
            'transaction_error_msg'),
        created_at=now()
    )))

    withdraw = gw_withdraw.get('cashWithdrawals_out').get('data_output')

    if isinstance(withdraw, dict):
        response_data.append({
            'account_number': request_data_gw.get('account_info').get('account_num'),
            'account_withdrawals_amount': request_data_gw.get('account_info').get('account_withdrawals_amount')
        })
    else:
        response_data.append({
            'account_number': request_data_gw.get('account_info').get('account_num'),
            'account_withdrawals_amount': withdraw
        })

    return ReposReturn(data=response_data)


async def repos_get_withdraw_info(booking_id: str, session: Session):
    get_withdraw_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()

    if not get_withdraw_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_ID_NOT_EXIST,
            detail='booking_id'
        )

    return ReposReturn(data=get_withdraw_info)


async def repos_get_acc_types(numbers: list, session: Session):
    get_acc_types = session.execute(
        select(
            CasaAccount.casa_account_number,
            CasaAccount.acc_type_id
        ).filter(CasaAccount.casa_account_number.in_(numbers))
    ).all()

    return ReposReturn(data=get_acc_types)
