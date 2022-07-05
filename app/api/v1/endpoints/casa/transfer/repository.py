from sqlalchemy import desc, select, update
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


@auto_commit
async def repos_save_casa_transfer_info(
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
):
    print('------------------------')
    print('booking_id')
    print(booking_id)
    print('------------------------')
    print('saving_transaction_stage_status')
    print(saving_transaction_stage_status)
    print('------------------------')
    print('saving_sla_transaction')
    print(saving_sla_transaction)
    print('------------------------')
    print('saving_transaction_stage')
    print(saving_transaction_stage)
    print('------------------------')
    print('saving_transaction_stage_phase')
    print(saving_transaction_stage_phase)
    print('------------------------')
    print('saving_transaction_stage_lane')
    print(saving_transaction_stage_lane)
    print('------------------------')
    print('saving_transaction_stage_role')
    print(saving_transaction_stage_role)
    print('------------------------')
    print('saving_transaction_daily')
    print(saving_transaction_daily)
    print('------------------------')
    print('saving_transaction_sender')
    print(saving_transaction_sender)
    print('------------------------')
    print('saving_transaction_job')
    print(saving_transaction_job)
    print('------------------------')
    print('saving_booking_business_form')
    print(saving_booking_business_form)
    print('------------------------')

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
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)
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


async def repos_get_casa_transfer_info(booking_id: str, session: Session):
    get_casa_transfer_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()
    return ReposReturn(data=get_casa_transfer_info)


async def repos_get_acc_types(numbers: list, session: Session):
    get_acc_types = session.execute(
        select(
            CasaAccount.casa_account_number,
            CasaAccount.acc_type_id
        ).filter(CasaAccount.casa_account_number.in_(numbers))
    ).all()

    return ReposReturn(data=get_acc_types)
