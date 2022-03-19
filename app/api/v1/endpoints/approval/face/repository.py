from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)


async def repos_get_approval_compare_faces(
    cif_id: str,
    session: Session
):
    """
    Lấy tất cả hình ảnh ở bước GTDD
    """
    customer_identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .filter(Customer.id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).first()

    _, customer_identity = customer_identities
    customer_identity_id = customer_identity.id
    face_compares = session.execute(
        select(
            CustomerCompareImage,
            CustomerCompareImageTransaction
        )
        .join(CustomerCompareImageTransaction,
              CustomerCompareImage.id == CustomerCompareImageTransaction.compare_image_id)
        .filter(CustomerCompareImage.identity_id == customer_identity_id)
        .order_by(desc(CustomerCompareImageTransaction.maker_at))
    ).all()

    if not face_compares:
        return ReposReturn(is_error=True, detail="No Face in Identity Step")

    return ReposReturn(data=face_compares)
