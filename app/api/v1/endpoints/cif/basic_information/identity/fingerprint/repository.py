import json

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    CompareFingerPrintRequest
)
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.master_data.identity import (
    FingerType, HandSide
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_GTDD_VT, IMAGE_TYPE_FINGERPRINT
)
from app.utils.error_messages import ERROR_NO_DATA
from app.utils.functions import now


@auto_commit
async def repos_save_fingerprint(
        cif_id: str,
        identity_id: str,
        log_data: json,
        session: Session,
        list_data_insert: list,
        created_by: str
) -> ReposReturn:
    # lấy list customer_identity_image theo vân tay
    customer_identity_image = session.execute(
        select(
            CustomerIdentityImage.id
        ).filter(
            and_(
                CustomerIdentityImage.identity_id == identity_id,
                CustomerIdentityImage.image_type_id == IMAGE_TYPE_FINGERPRINT
            )
        )
    ).scalars().all()
    # xóa list id vân tay
    if customer_identity_image:
        session.execute(
            delete(
                CustomerIdentityImage
            ).filter(CustomerIdentityImage.id.in_(customer_identity_image))
        )

    session.bulk_save_objects([CustomerIdentityImage(**data_insert) for data_insert in list_data_insert])

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
            HandSide,
            FingerType
        ).join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).join(
            HandSide, CustomerIdentityImage.hand_side_id == HandSide.id
        ).join(
            FingerType, CustomerIdentityImage.finger_type_id == FingerType.id
        ).filter(
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


async def repos_compare_finger_ekyc(cif_id: str, uuid: CompareFingerPrintRequest, session: Session):
    finger_print_ids = session.execute(
        select(
            CustomerIdentityImage.ekyc_id
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

    json_body = {
        "uuid": uuid.uuid,
        "id_fingers": finger_print_ids,
        "limit": 1
    }
    is_success, response = await service_ekyc.compare_finger_ekyc(cif_id=cif_id, json_body=json_body)

    return ReposReturn(data=response)
