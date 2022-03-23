from typing import List

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
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
    Output: Customer, CustomerIdentity, CustomerIdentityImage, CustomerCompareImage, CustomerCompareImageTransaction
    """
    customer_identities = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIdentityImage,
            # CustomerCompareImage,
            # CustomerCompareImageTransaction
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIdentityImage, and_(
            CustomerIdentity.id == CustomerIdentityImage.identity_id,
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FACE
        ))
        .filter(Customer.id == cif_id)
        .order_by(desc(CustomerIdentity.updater_at))
    ).all()
    if not customer_identities:
        return ReposReturn(is_error=True, detail="No Face in Identity Step")

    return ReposReturn(data=customer_identities)


@auto_commit
async def repos_save_approval_compare_face(
        saving_customer_compare_images: List,
        saving_customer_compare_image_transactions: List,
        session: Session
):
    """
    Lưu hình ảnh So sánh ở bước Phê duyệt
    """

    session.bulk_save_objects([
        CustomerCompareImage(**customer_compare_image)
        for customer_compare_image in saving_customer_compare_images
    ])
    session.bulk_save_objects([
        CustomerCompareImageTransaction(**customer_compare_image_transaction)
        for customer_compare_image_transaction in saving_customer_compare_image_transactions
    ])
    session.flush()

    return ReposReturn(data=None)
