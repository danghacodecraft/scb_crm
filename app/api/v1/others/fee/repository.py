from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.product import (
    ProductFee, ProductFeeBusiness
)


async def repos_get_fee_detail(fee_id: str, business_type_id: str, session: Session):
    fee_detail = session.execute(
        select(
            ProductFee,
            ProductFeeBusiness
        )
        .join(ProductFeeBusiness, and_(
            ProductFee.id == ProductFeeBusiness.product_fee_id,
            ProductFeeBusiness.business_type_id == business_type_id
        ))
        .filter(ProductFee.id == fee_id)
    ).scalar()
    return ReposReturn(data=fee_detail)
