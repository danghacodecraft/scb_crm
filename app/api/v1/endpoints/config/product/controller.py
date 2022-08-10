from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.product.repository import (
    repos_get_fee, repos_get_fee_category
)
from app.utils.functions import dropdown


class CtrConfigProduct(BaseController):
    async def ctr_product_fee_category_info(self, business_type_id: str):
        product_fee_category_info = self.call_repos(
            await repos_get_fee_category(
                session=self.oracle_session, business_type_id=business_type_id
            )
        )
        return self.response([dropdown(product_fee_category) for product_fee_category in product_fee_category_info])

    async def ctr_product_fee_info(self, category_id: str, business_type_id: str):
        product_fee_info = self.call_repos(
            await repos_get_fee(
                session=self.oracle_session, business_type_id=business_type_id, category_id=category_id
            )
        )
        return self.response([dropdown(product_fee) for product_fee in product_fee_info])
