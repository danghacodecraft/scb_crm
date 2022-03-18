from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.utils.constant.cif import ACTIVE_FLAG_ACTIVED
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST


async def repos_get_list_face(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerCompareImageTransaction
        )
        .join(CustomerCompareImage, CustomerCompareImageTransaction.compare_image_id == CustomerCompareImage.id)
        .join(CustomerIdentity, CustomerCompareImage.identity_id == CustomerIdentity.id)
        .join(
            Customer, and_(
                CustomerIdentity.customer_id == Customer.id,
                Customer.id == cif_id
            )
        ).order_by(
            desc(CustomerCompareImageTransaction.maker_at)
        ).filter(CustomerCompareImageTransaction.is_identity_compare == ACTIVE_FLAG_ACTIVED)
    ).scalars().all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    faces = [
        {
            "maker_at": compare_transaction.maker_at,
            "identity_image_id": compare_transaction.id,
            "image_url": compare_transaction.compare_image_url,
            "created_at": compare_transaction.maker_at,
            "similar_percent": compare_transaction.similar_percent
        } for compare_transaction in query_data
    ]

    return ReposReturn(data=faces)
