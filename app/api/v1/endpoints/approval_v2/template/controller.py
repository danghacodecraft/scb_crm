import json

from sqlalchemy.sql.functions import current_user

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval_v2.template.repository import (
    repos_get_template_data
)
from app.api.v1.endpoints.approval_v2.template.TKTT.controller import (
    CtrTemplateTKTT
)


class CtrTemplateDetail(BaseController):
    async def ctr_get_template_detail(self, template_id: str, booking_id: str):
        business_form_id__data = self.call_repos(
            await repos_get_template_data(
                template_id=template_id,
                booking_id=booking_id,
                session=self.oracle_session)
        )
        object_data = None
        for _, value in business_form_id__data.items():
            if isinstance(value, bytes):
                value = json.loads(value.decode('utf-8'))
            if not object_data:
                object_data = value
            else:
                object_data.update(value)
        template_detail_info = await CtrTemplateTKTT(current_user).ctr_get_template_nop_tien(
            object_data=object_data
        )
        return self.response(data=template_detail_info)
