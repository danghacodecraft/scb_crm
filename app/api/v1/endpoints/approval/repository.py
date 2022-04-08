from typing import List

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily, TransactionReceiver,
    TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    TransactionStage, TransactionStageLane, TransactionStagePhase,
    TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.cif import IMAGE_TYPE_FACE
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_approval_process(cif_id: str, session: Session) -> ReposReturn:
    trans_root_daily = aliased(TransactionDaily, name='TransactionDaily')

    transactions = session.execute(
        select(
            BookingCustomer,
            Booking,
            TransactionDaily,
            TransactionSender,
            trans_root_daily
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .join(
            trans_root_daily,
            trans_root_daily.transaction_root_id == TransactionDaily.transaction_root_id
        )
        .filter(BookingCustomer.customer_id == cif_id)
        .order_by(desc(trans_root_daily.created_at))
    ).all()

    if not transactions:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=transactions)


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
        is_stage_init: bool,
        session: Session
):
    saving_transaction_daily_parent_id = None
    saving_transaction_daily_root_id = saving_transaction_daily['transaction_id']

    if not is_stage_init:
        # Lấy thông tin Transaction Daily trước đó
        _, _, previous_transaction_daily = session.execute(
            select(
                BookingCustomer,
                Booking,
                TransactionDaily
            )
            .join(Booking, BookingCustomer.booking_id == Booking.id)
            .outerjoin(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
            .filter(BookingCustomer.customer_id == cif_id)
        ).first()

        saving_transaction_daily_parent_id = previous_transaction_daily.transaction_id
        saving_transaction_daily_root_id = previous_transaction_daily.transaction_root_id

    saving_transaction_daily.update(dict(
        transaction_parent_id=saving_transaction_daily_parent_id,
        transaction_root_id=saving_transaction_daily_root_id,
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


async def repos_get_approval_identity_image(
    cif_id: str,
    image_type_id: str,
    identity_type: str,
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
            CustomerIdentityImage.image_type_id == image_type_id
        ))
        .filter(CustomerIdentity.customer_id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).all()
    if not customer_identities:
        return ReposReturn(is_error=True, detail=f"No {identity_type} in Identity Step")

    return ReposReturn(data=customer_identities)
