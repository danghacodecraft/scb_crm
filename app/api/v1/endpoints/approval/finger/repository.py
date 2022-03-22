from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import IMAGE_TYPE_FINGERPRINT
from app.utils.error_messages import ERROR_NO_DATA


async def repos_get_data_finger(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentityImage,
            CustomerIdentityImageTransaction,
            HandSide,
            FingerType
        )
        .join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        )
        .join(CustomerIdentityImageTransaction, CustomerIdentityImage.id == CustomerIdentityImageTransaction.identity_image_id)
        .join(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .join(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
        ).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="cif_id")

    return ReposReturn(data=query_data)
