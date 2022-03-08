import json

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_GTDD_CK, IMAGE_TYPE_CODE_SIGNATURE
)
from app.utils.error_messages import ERROR_SIGNATURE_IS_NULL
from app.utils.functions import now


@auto_commit
async def repos_save_signature(
        cif_id: str,
        list_data_insert: list,
        log_data: json,
        session: Session,
        created_by: str
) -> ReposReturn:

    session.bulk_save_objects([CustomerIdentityImage(**data_insert) for data_insert in list_data_insert])

    await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_TTCN_GTDD_CK
    )

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_get_signature_data(cif_id: str, session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            CustomerIdentityImage
        ).join(
            CustomerIdentity, and_(
                CustomerIdentityImage.identity_id == CustomerIdentity.id,
                CustomerIdentity.customer_id == cif_id
            )
        ).filter(
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SIGNATURE
        ).order_by(desc(CustomerIdentityImage.maker_at))
    ).scalars().all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_SIGNATURE_IS_NULL, loc=f"cif_id: {cif_id}")

    return ReposReturn(data=query_data)
