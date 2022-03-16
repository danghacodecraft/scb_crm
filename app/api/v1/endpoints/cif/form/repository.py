from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily, TransactionReceiver,
    TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    TransactionStage, TransactionStageLane, TransactionStagePhase,
    TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.cif import CIF_ID_TEST
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_approval_process(cif_id: str) -> ReposReturn:
    if cif_id == CIF_ID_TEST:
        return ReposReturn(data=[
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]

            },
            {

                "created_date": "string",
                "logs":

                    [

                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        },
                        {
                            "user_id": "string",
                            "full_name": "string",
                            "user_avatar_url": "string",
                            "id": "string",
                            "created_at": "2019-08-24T14:15:22Z",
                            "content": "string"
                        }
                    ]
            }
        ]
        )
    else:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')


@auto_commit
async def repos_approve(
        cif_id: str,
        saving_transaction_stage_status: dict,
        saving_transaction_stage: dict,
        saving_transaction_daily: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_sender: dict,
        saving_transaction_receiver: dict,
        session: Session
):

    # Lấy thông tin Transaction Daily trước đó
    _, _, previous_transaction_daily = session.execute(
        select(
            BookingCustomer,
            Booking,
            TransactionDaily
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).first()

    saving_transaction_parent_id = previous_transaction_daily.transaction_id
    saving_transaction_root_id = previous_transaction_daily.transaction_root_id
    saving_transaction_daily.update(dict(
        transaction_parent_id=saving_transaction_parent_id,
        transaction_root_id=saving_transaction_root_id,
    ))

    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        TransactionDaily(**saving_transaction_daily),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionSender(**saving_transaction_sender),
        TransactionReceiver(**saving_transaction_receiver)
    ])

    # Cập nhật lại TransactionDaily mới cho Booking
    booking_customer, booking = session.execute(
        select(
            BookingCustomer,
            Booking
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).first()
    booking.transaction_id = saving_transaction_daily['transaction_id']

    return ReposReturn(data={
        "cif_id": cif_id
    })
