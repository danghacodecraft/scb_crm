from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
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


async def repos_check_account_num(account_num, session: Session) -> ReposReturn:
    account_info = session.execute(
        select(CasaAccount.casa_account_number)
        .filter(CasaAccount.casa_account_number == account_num)
    ).scalar()

    return ReposReturn(data=account_info)


@auto_commit
async def repos_save_open_sec_info(
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
        session: Session
) -> ReposReturn:
    insert_list = [
        # Tạo BOOKING, CRM_TRANSACTION_DAILY -> CRM_BOOKING -> BOOKING_CUSTOMER -> BOOKING_BUSINESS_FORM
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)
    ]
    # Lưu log vào DB
    session.add_all(insert_list)
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
