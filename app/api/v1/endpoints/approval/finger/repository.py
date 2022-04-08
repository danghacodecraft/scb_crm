from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage, CustomerIdentityImageTransaction
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
        .join(CustomerIdentityImageTransaction,
              CustomerIdentityImage.id == CustomerIdentityImageTransaction.identity_image_id)
        .join(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .join(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
        ).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="cif_id")

    return ReposReturn(data=query_data)


async def repos_compare_finger_ekyc(
        cif_id: str,
        uuid_ekyc: str,
        id_fingers: list
):
    json_body = {
        "uuid": uuid_ekyc,
        "id_fingers": id_fingers,
        "limit": len(id_fingers)
    }
    is_success, response = await service_ekyc.compare_finger_ekyc(cif_id=cif_id, json_body=json_body)
    if not is_success:
        return ReposReturn(is_error=True, msg=response['message'], loc="COMPARE_FINGERPRINT")
    return ReposReturn(data=response)


@auto_commit
async def repos_save_compare_finger(
        compare_images: List,
        compare_image_transactions: List,
        session: Session
):
    session.bulk_save_objects([
        CustomerCompareImage(**customer_compare_image)
        for customer_compare_image in compare_images
    ])
    session.bulk_save_objects([
        CustomerCompareImageTransaction(**customer_compare_image_transaction)
        for customer_compare_image_transaction in compare_image_transactions
    ])

    return ReposReturn(data=None)


async def repos_get_id_finger_ekyc(cif_id: str, session: Session):
    finger_print_ids = session.execute(
        select(
            CustomerIdentityImage
        )
        .join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        )
        .filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
        )
    ).scalars().all()

    if not finger_print_ids:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA)

    return ReposReturn(data=finger_print_ids)
