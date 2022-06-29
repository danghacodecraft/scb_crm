from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.cif import BUSINESS_FORM_CLOSE_CASA
from app.utils.functions import now


async def repos_save_close_casa_account(
        booking_id,
        saving_transaction_stage_status,
        saving_transaction_stage,
        saving_transaction_stage_lane,
        saving_sla_transaction,
        saving_transaction_stage_phase,
        saving_transaction_stage_role,
        saving_transaction_daily,
        saving_transaction_sender,
        request_json,
        session: Session
) -> ReposReturn:

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
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_CLOSE_CASA,
            save_flag=True,
            created_at=now()
        ))
    ])
    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )
    session.flush()
    return ReposReturn(data=booking_id)
