from typing import List, Optional

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, BookingCustomer, TransactionDaily,
    TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    BusinessJob, BusinessType, SlaTransaction, TransactionJob,
    TransactionStage, TransactionStageAction, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_INIT_CIF,
    BUSINESS_TYPE_OPEN_CASA, BUSINESS_TYPES
)
from app.utils.constant.cif import IMAGE_TYPE_FACE
from app.utils.error_messages import (
    ERROR_BOOKING_ID_NOT_EXIST, ERROR_BOOKING_TRANSACTION_NOT_EXIST
)


async def repos_get_approval_process(booking_id: str, session: Session) -> ReposReturn:
    booking = session.execute(
        select(
            Booking
        ).filter(Booking.id == booking_id)
    ).scalar()
    if not booking:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_ID_NOT_EXIST, loc=f'header -> booking_id: {booking_id}')

    transactions = []
    trans_root_daily = aliased(TransactionDaily, name='TransactionDaily')

    if booking.business_type_id == BUSINESS_TYPE_INIT_CIF:
        transactions = session.execute(
            select(
                BookingCustomer,
                Booking,
                TransactionDaily,
                TransactionSender,
                trans_root_daily
            )
            .join(BookingCustomer, BookingCustomer.booking_id == Booking.id)
            .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
            .join(
                trans_root_daily,
                trans_root_daily.transaction_root_id == TransactionDaily.transaction_root_id
            )
            .join(TransactionSender, trans_root_daily.transaction_id == TransactionSender.transaction_id)
            .filter(Booking.id == booking_id)
            .order_by(desc(trans_root_daily.created_at))
        ).all()

    if booking.business_type_id == BUSINESS_TYPE_OPEN_CASA or booking.business_type_id == BUSINESS_TYPE_AMOUNT_BLOCK:
        transactions = session.execute(
            select(
                TransactionDaily,
                TransactionDaily,
                TransactionDaily,
                TransactionSender,
                trans_root_daily
            )
            .join(
                trans_root_daily,
                trans_root_daily.transaction_root_id == TransactionDaily.transaction_root_id
            )
            .join(TransactionSender, trans_root_daily.transaction_id == TransactionSender.transaction_id)
            .filter(TransactionDaily.transaction_id == booking.transaction_id)
        ).all()

    if not transactions:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_TRANSACTION_NOT_EXIST, loc=f'booking_id: {booking_id}')

    return ReposReturn(data=transactions)


@auto_commit
async def repos_approve(
        cif_id: str,
        business_type_id: str,
        booking_id: str,
        saving_transaction_stage_status: dict,
        saving_transaction_stage_action: dict,
        # saving_sla_transaction: dict,
        saving_transaction_stage: dict,
        saving_transaction_daily: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_sender: dict,
        # saving_transaction_receiver: dict,
        is_stage_init: bool,
        session: Session
):
    saving_transaction_daily_parent_id = None
    saving_transaction_daily_root_id = saving_transaction_daily['transaction_id']

    if not is_stage_init:
        previous_transaction_daily = None
        # Lấy thông tin Transaction Daily trước đó
        _, previous_transaction_daily = session.execute(
            select(
                Booking,
                TransactionDaily
            )
            .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
            .filter(Booking.id == booking_id)
        ).first()

        if not previous_transaction_daily:
            return ReposReturn(is_error=True, msg="No Previous Transaction Daily")

        saving_transaction_daily_parent_id = previous_transaction_daily.transaction_id
        saving_transaction_daily_root_id = previous_transaction_daily.transaction_root_id

    saving_transaction_daily.update(dict(
        transaction_parent_id=saving_transaction_daily_parent_id,
        transaction_root_id=saving_transaction_daily_root_id,
    ))

    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStageAction(**saving_transaction_stage_action),
        # SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionDaily(**saving_transaction_daily),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionSender(**saving_transaction_sender)
    ])

    if business_type_id not in BUSINESS_TYPES:
        return ReposReturn(is_error=True, msg=f"business_type_id={business_type_id} not in {BUSINESS_TYPES}")

    # Cập nhật lại TransactionDaily mới cho Booking
    session.execute(
        update(
            Booking
        )
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )

    return ReposReturn(data={
        "cif_id": cif_id
    })


async def repos_approval_get_face_authentication(
        cif_id: str,
        session: Session
):

    face_authentication = session.execute(
        select(
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerIdentityImageTransaction,
            CustomerCompareImage,
            CustomerCompareImageTransaction
        )
        .join(CustomerIdentityImage, and_(
            CustomerIdentity.id == CustomerIdentityImage.identity_id
        ))
        .join(
            CustomerIdentityImageTransaction,
            CustomerIdentityImage.id == CustomerIdentityImageTransaction.identity_image_id
        )
        .join(CustomerCompareImage, CustomerIdentityImage.id == CustomerCompareImage.identity_image_id)
        .join(
            CustomerCompareImageTransaction,
            CustomerCompareImage.id == CustomerCompareImageTransaction.compare_image_id
        )
        .filter(CustomerIdentity.customer_id == cif_id)
        .order_by(desc(CustomerCompareImageTransaction.maker_at))
    ).all()

    return ReposReturn(data=face_authentication)


async def repos_get_approval_identity_faces(
    cif_id: str,
    session: Session
):
    """
    Lấy tất cả hình ảnh ở bước GTDD
    Output: CustomerIdentity, CustomerIdentityImage
    """
    customer_identities = session.execute(
        select(
            CustomerIdentity,
            CustomerIdentityImage
        )
        .join(CustomerIdentityImage, and_(
            CustomerIdentity.id == CustomerIdentityImage.identity_id,
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FACE
        ))
        .filter(CustomerIdentity.customer_id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).all()
    if not customer_identities:
        return ReposReturn(is_error=True, detail="No Face in Identity Step")

    return ReposReturn(data=customer_identities)


async def repos_get_approval_identity_faces_by_url(
    url: str,
    session: Session
):
    data = session.execute(
        select(
            CustomerIdentityImage
        )
        .filter(CustomerIdentityImage.image_url == url)
    ).scalars().all()
    return ReposReturn(data=data)


async def repos_get_compare_image_transactions(
    identity_image_ids: List,
    session: Session
):
    compare_image_transactions = session.execute(
        select(
            CustomerCompareImage,
            CustomerCompareImageTransaction
        )
        .join(CustomerCompareImageTransaction, CustomerCompareImage.id == CustomerCompareImageTransaction.compare_image_id)
        .filter(CustomerCompareImage.identity_image_id.in_(identity_image_ids))
        .order_by(desc(CustomerCompareImage.maker_at))
    ).all()

    return ReposReturn(data=compare_image_transactions)


async def repos_get_approval_identity_images_by_image_type_id(
    cif_id: str,
    image_type_id: str,
    identity_type: str,
    session: Session
):
    """
    Lấy tất cả hình ảnh ở bước GTDD bằng image_type_id
    Output: CustomerIdentity, CustomerIdentityImage
    """
    customer_identities = session.execute(
        select(
            CustomerIdentity,
            CustomerIdentityImage
        )
        .join(CustomerIdentityImage, and_(
            CustomerIdentity.id == CustomerIdentityImage.identity_id,
            CustomerIdentityImage.image_type_id == image_type_id
        ))
        .filter(CustomerIdentity.customer_id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).all()
    if not customer_identities:
        return ReposReturn(is_error=True, detail=f"No {identity_type} in Identity Step")

    return ReposReturn(data=customer_identities)


async def repos_get_approval_identity_images(
    cif_id: str,
    session: Session
):
    """
    Lấy tất cả hình ảnh ở bước GTDD
    Output: CustomerIdentity, CustomerIdentityImage
    """
    customer_identities = session.execute(
        select(
            CustomerIdentity,
            CustomerIdentityImage
        )
        .join(CustomerIdentityImage, and_(
            CustomerIdentity.id == CustomerIdentityImage.identity_id
        ))
        .filter(CustomerIdentity.customer_id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).all()

    return ReposReturn(data=customer_identities)


async def repos_get_transaction_daily(
    cif_id: str,
    session: Session
):
    transaction_daily = session.execute(
        select(
            TransactionDaily,
            BookingCustomer,
            Booking
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).scalar()
    if not transaction_daily:
        return ReposReturn(is_error=True, msg="No transaction daily")
    transaction_root_id = transaction_daily.transaction_root_id
    transaction_daily = session.execute(
        select(
            TransactionSender,
            TransactionDaily,
            TransactionStage
        )
        .join(TransactionStage, and_(
            TransactionDaily.transaction_stage_id == TransactionStage.id,
            TransactionStage.transaction_stage_phase_code == "KHOI_TAO_HO_SO"
        ))
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .filter(TransactionDaily.transaction_root_id == transaction_root_id)
        .order_by(desc(TransactionDaily.created_at))
    ).scalars().first()
    return ReposReturn(data=transaction_daily)


async def repos_get_list_audit(session: Session):
    list_supervisor = session.execute(
        select(
            Booking.code,
            BusinessType,
            Customer.cif_number,
            Customer.full_name_vn,
            Customer.mobile_number,
            CustomerIdentity.id,
            CustomerIdentity.identity_type_id,
            TransactionDaily.transaction_id,
            TransactionStage.id,
            TransactionStage.transaction_stage_phase_code,
            TransactionStage.transaction_stage_phase_name,
            TransactionStageStatus.id,
            TransactionStageStatus.code,
            TransactionStageStatus.name,
            BookingCustomer
        )
        .join(BusinessType, Booking.business_type_id == BusinessType.id)
        .join(BookingCustomer, Booking.id == BookingCustomer.booking_id)
        .join(Customer, BookingCustomer.customer_id == Customer.id)
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, and_(
            TransactionDaily.transaction_stage_id == TransactionStage.id,
            TransactionStage.transaction_stage_phase_code == "PHE_DUYET_KSV",
            TransactionStage.is_reject is False
        ))
        .join(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)
    ).all()

    list_audit = session.execute(
        select(
            Booking.code,
            BusinessType,
            Customer.cif_number,
            Customer.full_name_vn,
            Customer.mobile_number,
            CustomerIdentity.id,
            CustomerIdentity.identity_type_id,
            TransactionDaily.transaction_id,
            TransactionStage.id,
            TransactionStage.transaction_stage_phase_code,
            TransactionStage.transaction_stage_phase_name,
            TransactionStageStatus.id,
            TransactionStageStatus.code,
            TransactionStageStatus.name,
            BookingCustomer
        )
        .join(BusinessType, Booking.business_type_id == BusinessType.id)
        .join(BookingCustomer, Booking.id == BookingCustomer.booking_id)
        .join(Customer, BookingCustomer.customer_id == Customer.id)
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, and_(
            TransactionDaily.transaction_stage_id == TransactionStage.id,
            TransactionStage.transaction_stage_phase_code == "PHE_DUYET_KSS"
        ))
        .join(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)
        .distinct()
    ).all()
    return ReposReturn(data=list_audit + list_supervisor)


async def repos_get_business_jobs(session: Session, cif_id: str):
    business_jobs = session.execute(
        select(
            TransactionJob,
            BookingCustomer
        )
        .join(TransactionJob, BookingCustomer.booking_id == TransactionJob.booking_id)
        .filter(BookingCustomer.customer_id == cif_id)
        .order_by(TransactionJob.created_at)
    ).scalars().all()
    return ReposReturn(data=business_jobs)


async def repos_get_business_jobs_by_open_casa(booking_id: str, session: Session):
    business_jobs = session.execute(
        select(
            TransactionJob,
            Booking
        )
        .join(TransactionJob, Booking.id == TransactionJob.booking_id)
        .filter(Booking.id == booking_id)
    ).scalars().all()
    return ReposReturn(data=business_jobs)


async def repos_get_business_job_codes(business_type_code: str, session: Session):
    business_job_codes = session.execute(
        select(
            BusinessJob
        )
        .filter(and_(
            BusinessJob.business_type_id == business_type_code,
            BusinessJob.active_flag == 1
        ))
    ).scalars().all()
    return ReposReturn(data=business_job_codes)


async def repos_get_booking_business_form_by_booking_id(
        booking_id: str,
        session: Session,
        business_form_id: Optional[str] = None
):
    business_form = session.execute(
        select(
            BookingBusinessForm
        ).filter(and_(
            BookingBusinessForm.booking_id == booking_id,
            BookingBusinessForm.business_form_id == business_form_id
        ))
    ).scalar()

    return ReposReturn(data=business_form)
