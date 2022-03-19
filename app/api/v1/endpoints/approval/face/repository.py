from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage
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
    face_compares = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIdentityImage,
            CustomerCompareImage,
            CustomerCompareImageTransaction
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerCompareImage, CustomerIdentity.id == CustomerCompareImage.identity_id)
        .join(CustomerCompareImageTransaction,
              CustomerCompareImage.id == CustomerCompareImageTransaction.compare_image_id)
        .filter(Customer.id == cif_id)
        .order_by(desc(CustomerCompareImageTransaction.maker_at))
    ).all()

    if not face_compares:
        return ReposReturn(is_error=True, detail="No Face in Identity Step")

    return ReposReturn(data=face_compares)
