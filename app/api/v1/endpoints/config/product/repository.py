from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.product import (
    ProductFee, ProductFeeBusiness, ProductFeeCategory
)


async def repos_get_fee_category(business_type_id: str, session: Session):
    product_fee_category_info = session.execute(
        select(
            ProductFeeCategory,
            ProductFeeBusiness.category_id
        )
        .join(ProductFeeCategory, ProductFeeBusiness.category_id == ProductFeeCategory.id)
        .filter(ProductFeeBusiness.business_type_id == business_type_id)
        .distinct(ProductFeeBusiness.category_id)
    ).scalars().all()
    return ReposReturn(data=product_fee_category_info)


async def repos_get_fee(business_type_id: str, category_id: str, session: Session):
    product_fee_category_info = session.execute(
        select(
            ProductFee,
            ProductFeeBusiness
        )
        .join(ProductFee, ProductFeeBusiness.product_fee_id == ProductFee.id)
        .filter(and_(
            ProductFeeBusiness.category_id == category_id,
            ProductFeeBusiness.business_type_id == business_type_id
        ))
    ).scalars().all()
    return ReposReturn(data=product_fee_category_info)
