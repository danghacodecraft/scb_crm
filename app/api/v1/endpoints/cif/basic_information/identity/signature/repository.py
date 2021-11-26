from typing import List

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.utils.error_messages import ERROR_SIGNATURE_IS_NULL
from app.utils.functions import datetime_to_date, now


async def repos_save_signature(cif_id: str, list_data_insert: List, session: Session, created_by: str) -> ReposReturn:

    data_insert = [CustomerIdentityImage(**data_insert) for data_insert in list_data_insert]
    session.bulk_save_objects(data_insert)
    session.commit()

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
            CustomerIdentityImage.finger_type_id.is_(None),
            CustomerIdentityImage.hand_side_id.is_(None),
            CustomerIdentityImage.vector_data.is_(None)
        ).order_by(desc(CustomerIdentityImage.maker_at))
    ).scalars().all()

    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_SIGNATURE_IS_NULL, loc=f"cif_id: {cif_id}")

    date__signatures = {}
    for customer_identity_image in query_data:
        date_str = datetime_to_date(customer_identity_image.maker_at)

        if date_str not in date__signatures:
            date__signatures[date_str] = []

        date__signatures[date_str].append(
            {
                'identity_image_id': customer_identity_image.id,
                'image_url': customer_identity_image.image_url,
                'active_flag': customer_identity_image.active_flag
            }
        )

    data_response = [{
        'created_date': data_str,
        'signature': signature
    } for data_str, signature in date__signatures.items()]

    return ReposReturn(data=data_response)
