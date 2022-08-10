from app.api.base.controller import BaseController
from app.api.v1.endpoints.config.product.repository import (
    repos_get_fee_category
)
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.product import ProductFee
from app.utils.functions import dropdown


class CtrConfigProduct(BaseController):
    async def ctr_product_fee_category_info(self, business_type_id: str):
        product_fee_category_info = self.call_repos(
            await repos_get_fee_category(
                session=self.oracle_session, business_type_id=business_type_id
            )
        )
        return self.response([dropdown(product_fee_category) for product_fee_category in product_fee_category_info])

    async def ctr_product_fee_info(self, category_id: str):
        product_fee_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=ProductFee, category_id=category_id
            )
        )
        return self.response(product_fee_info)
