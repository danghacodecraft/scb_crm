from typing import List

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.e_banking.model import (
    TdAccount, TdAccountResign
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer,
    TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)


@auto_commit
async def repos_save_td_account(
        booking_id,
        td_accounts: List,
        td_account_resigns: List,
        saving_booking_account,
        saving_booking_customer,
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
    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form),
    ])
    session.bulk_save_objects([TdAccount(**item) for item in td_accounts])
    session.bulk_save_objects([TdAccountResign(**item) for item in td_account_resigns])
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
async def repos_update_td_account(
    booking_id: str,
    update_td_account: List[dict],
    # saving_booking_business_form: dict,
    session: Session
):
    session.bulk_update_mappings(TdAccount, update_td_account)
    # session.add(BookingBusinessForm(**saving_booking_business_form))

    return ReposReturn(data=booking_id)


async def repos_get_deposit_pay_in(
    booking_id: str
):
    return ReposReturn(data=booking_id)
