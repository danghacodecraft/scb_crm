import json

from sqlalchemy import select, desc, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm, TransactionDaily, TransactionSender, \
    Booking
from app.third_parties.oracle.models.master_data.others import TransactionStageStatus, TransactionStage, SlaTransaction, \
    TransactionStageLane, TransactionStagePhase, TransactionStageRole, TransactionJob
from app.utils.constant.approval import BUSINESS_JOB_CODE_START_CASA_TOP_UP
from app.utils.constant.cif import BUSINESS_FORM_CASA_TOP_UP
from app.utils.functions import now, generate_uuid


# @auto_commit
async def repos_save_casa_top_up_info(
        booking_id: str,
        saving_transaction_stage_status: dict,
        saving_sla_transaction: dict,
        saving_transaction_stage: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        request_json: json,
        history_datas: json,
        session: Session
):
    # Lưu log vào DB
    session.add_all([
        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSINESS_FORM
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_START_CASA_TOP_UP,
            complete_flag=True,
            error_code=None,
            error_desc=None,
            created_at=now()
        )),
        BookingBusinessForm(
            booking_id=booking_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_CASA_TOP_UP,
            created_at=now(),
            save_flag=True,
            log_data=history_datas
        )
    ])

    # Update Booking
    session.execute(
        update(
            Booking
        )
        .filter(Booking.id == booking_id)
        .values(
            transaction_id=saving_transaction_daily['transaction_id']
        )
    )
    session.flush()
    return ReposReturn(data=booking_id)


async def repos_get_casa_top_up_info(booking_id: str, session: Session):
    get_casa_top_up_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()
    return ReposReturn(data=get_casa_top_up_info)
