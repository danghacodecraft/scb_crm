import json

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_CREATE_FINGERPRINT, BUSINESS_FORM_TTCN_GTDD_VT,
    IMAGE_TYPE_FINGERPRINT
)
from app.utils.error_messages import ERROR_NO_DATA
from app.utils.functions import now


async def repos_get_identity_image(
        identity_id: str,
        session: Session,
):
    customer_identity_image = session.execute(
        select(
            CustomerIdentityImage
        ).filter(
            and_(
                CustomerIdentityImage.identity_id == identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
            )
        )
    ).scalars().all()

    return ReposReturn(data=customer_identity_image)


@auto_commit
async def repos_save_fingerprint(
        cif_id: str,
        is_create: bool,
        log_data: json,
        session: Session,
        save_identity_image: list,
        save_identity_image_transaction: list,
        update_identity_image: list,
        created_by: str
) -> ReposReturn:
    # update active_flag identity_image
    if not is_create:
        session.bulk_update_mappings(CustomerIdentityImage, update_identity_image)

    # tạo identity_image từ request
    session.bulk_save_objects([CustomerIdentityImage(**identity_image) for identity_image in save_identity_image])
    # tạo identity_image_transaction từ request
    session.bulk_save_objects(
        [CustomerIdentityImageTransaction(**identity_image_transaction) for identity_image_transaction in
         save_identity_image_transaction])

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TTCN_GTDD_VT
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


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
        .join(
            CustomerIdentityImageTransaction, and_(
                CustomerIdentityImage.id == CustomerIdentityImageTransaction.identity_image_id,
                # query lấy vân tay từ transaction_image với identity_image active_flag = 1
                CustomerIdentityImage.active_flag == ACTIVE_FLAG_CREATE_FINGERPRINT
            )
        )
        .join(HandSide, CustomerIdentityImage.hand_side_id == HandSide.id)
        .join(FingerType, CustomerIdentityImage.finger_type_id == FingerType.id)
        .filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
        ).order_by(CustomerIdentityImage.finger_type_id)
    ).all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="cif_id")

    return ReposReturn(data=query_data)


async def repos_add_finger_ekyc(cif_id: str, uuid: str):
    json_body = {
        "uuid": uuid
    }
    is_success, response = await service_ekyc.add_finger_ekyc(cif_id=cif_id, json_body=json_body)

    return ReposReturn(data=response['id'])
