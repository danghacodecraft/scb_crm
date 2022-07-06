from sqlalchemy import select, desc, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.contact.model import CustomerAddress
from app.third_parties.oracle.models.cif.basic_information.identity.model import CustomerIdentity
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm, TransactionDaily, TransactionSender, \
    Booking
from app.third_parties.oracle.models.master_data.others import TransactionStageStatus, TransactionStage, SlaTransaction, \
    TransactionStageLane, TransactionStagePhase, TransactionStageRole, TransactionJob


@auto_commit
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
        saving_transaction_job: dict,
        saving_booking_business_form: dict,
        # saving_customer: dict,
        # saving_customer_identity: dict,
        # saving_customer_address: dict,
        session: Session
):
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

    # if saving_customer and saving_customer_identity and saving_customer_address:
    #     insert_list.extend([
    #         Customer(**saving_customer),
    #         CustomerIdentity(**saving_customer_identity),
    #         CustomerAddress(**saving_customer_address)
    #         BookingCustomer(
    #             booking_id=booking_id,
    #             customer_id=saving_customer['id']
    #         )
    #     ])

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


async def repos_get_casa_top_up_info(booking_id: str, session: Session):
    get_casa_top_up_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()
    return ReposReturn(data=get_casa_top_up_info)
