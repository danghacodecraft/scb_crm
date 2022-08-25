import json

from app.api.base.controller import BaseController
from app.api.base.schema import ResponseData
from app.api.v1.endpoints.approval_v2.template.repository import (
    repos_get_template_data
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    TMSCasaTopUpResponse
)
from app.api.v1.endpoints.approval_v2.template.withdraw.schema import (
    TMSWithdrawResponse
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_CASA_TOP_UP, BUSINESS_TYPE_WITHDRAW
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

        if object_data['business_type_id'] == BUSINESS_TYPE_CASA_TOP_UP:
            object_data = ResponseData[TMSCasaTopUpResponse](**self.response(data=object_data))

        if object_data['business_type_id'] == BUSINESS_TYPE_WITHDRAW:
            object_data = ResponseData[TMSWithdrawResponse](**self.response(data=object_data))
        return object_data
