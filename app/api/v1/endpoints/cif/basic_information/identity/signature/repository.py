import json

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.settings.event import service_ekyc
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerCompareImage, CustomerCompareImageTransaction, CustomerIdentity,
    CustomerIdentityImage, CustomerIdentityImageTransaction
)
from app.utils.constant.cif import (
    ACTIVE_FLAG_DISACTIVED, BUSINESS_FORM_TTCN_GTDD_CK,
    IMAGE_TYPE_CODE_SIGNATURE
)
from app.utils.error_messages import ERROR_SIGNATURE_IS_NULL
from app.utils.functions import generate_uuid, now


@auto_commit
async def repos_save_signature(
        cif_id: str,
        save_identity_image: list,
        save_identity_image_transaction: list,
        log_data: json,
        session: Session,
        created_by: str
) -> ReposReturn:
    session.bulk_save_objects([CustomerIdentityImage(**data_insert) for data_insert in save_identity_image])
    session.bulk_save_objects(
        [CustomerIdentityImageTransaction(**data_insert) for data_insert in save_identity_image_transaction]
    )

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TTCN_GTDD_CK
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_signature_data(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentityImageTransaction
        )
        .join(CustomerIdentityImage, CustomerIdentityImageTransaction.identity_image_id == CustomerIdentityImage.id)
        .join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SIGNATURE
        ).order_by(desc(CustomerIdentityImageTransaction.maker_at))
    ).scalars().all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_SIGNATURE_IS_NULL, loc=f"cif_id: {cif_id}")

    return ReposReturn(data=query_data)


@auto_commit
async def repos_compare_signature(cif_id: str, uuid_ekyc: str, session: Session, user_id: str) -> ReposReturn:
    signature_query = session.execute(
        select(
            CustomerIdentityImage
        )
        .join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SIGNATURE
        ).order_by(desc(CustomerIdentityImage.maker_at))
    ).scalars().all()

    if not signature_query:
        return ReposReturn(is_error=True, msg='ERROR_NO_DATA')

    signature_compares = []

    for signature in signature_query:

        is_success, response = await service_ekyc.compare_signature(
            cif_id=cif_id,
            uuid_ekyc=uuid_ekyc,
            sign_uuid=signature.ekyc_uuid
        )

        if is_success:
            response.update({
                "image_url": signature.image_url
            })
            signature_compares.append(response)
            data_compare_image = {
                "id": generate_uuid(),
                "identity_id": signature.identity_id,
                "identity_image_id": signature.id,
                "compare_image_url": uuid_ekyc,
                "similar_percent": response['similarity_percent'],
                "maker_id": user_id,
                "maker_at": now()
            }
            data_compare_image_trans = {
                "compare_image_id": data_compare_image['id'],
                "identity_image_id": data_compare_image['identity_image_id'],
                "is_identity_compare": ACTIVE_FLAG_DISACTIVED,
                "compare_image_url": data_compare_image['compare_image_url'],
                "similar_percent": data_compare_image['similar_percent'],
                "maker_id": data_compare_image['maker_id'],
                "maker_at": data_compare_image['maker_at']
            }
            session.add_all([
                CustomerCompareImage(**data_compare_image),
                CustomerCompareImageTransaction(**data_compare_image_trans),
            ])

    return ReposReturn(data=signature_compares)
