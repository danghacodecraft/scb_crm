import json
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
from app.utils.constant.approval import BUSINESS_JOB_CODE_START_OPEN_TD_ACCOUNT
from app.utils.constant.cif import BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT
from app.utils.functions import generate_uuid, now


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
        request_json: json,
        history_datas: json,
        session: Session
):
    session.bulk_save_objects([TdAccount(**item) for item in td_accounts])

    session.bulk_save_objects([TdAccountResign(**item) for item in td_account_resigns])
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
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT,
            save_flag=True,
            created_at=now(),
            log_data=history_datas
        )),
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_START_OPEN_TD_ACCOUNT,
            complete_flag=True,
            error_code=None,
            error_desc=None,
            created_at=now()
        ))
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
