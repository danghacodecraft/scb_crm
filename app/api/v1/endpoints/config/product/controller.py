from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.product import (
    ProductFeeCategory
)


class CtrConfigProduct(BaseController):
    async def ctr_product_fee_category_info(self):
        account_fee_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=ProductFeeCategory
            )
        )
        return self.response(account_fee_info)
