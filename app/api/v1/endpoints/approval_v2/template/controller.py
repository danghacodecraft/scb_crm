from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval_v2.template.repository import (
    repos_get_template_data
)


class CtrTemplateDetail(BaseController):
    async def ctr_get_template_detail(self, template_id: str, booking_id: str):
        objetc_json = self.call_repos(
            await repos_get_template_data(
                template_id=template_id,
                booking_id=booking_id,
                session=self.oracle_session)
        )
        return self.response(data=objetc_json)
