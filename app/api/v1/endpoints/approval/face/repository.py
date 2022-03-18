from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.constant.cif import IMAGE_TYPE_FACE


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
        .join(CustomerIdentityImage, and_(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FACE,
            CustomerIdentity.id == CustomerIdentityImage.identity_id
        ))
        .join(CustomerCompareImageTransaction,
              CustomerIdentityImage.id == CustomerCompareImageTransaction.identity_image_id)
        .filter(Customer.id == cif_id)
        .order_by(desc(CustomerCompareImageTransaction.maker_at))
    ).all()

    return ReposReturn(data=face_compares)
