from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.others import BusinessType


class CtrConfigDashboard(BaseController):
    async def ctr_get_business_types(self):
        business_types = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=BusinessType
            )
        )
        return self.response(data=business_types)
