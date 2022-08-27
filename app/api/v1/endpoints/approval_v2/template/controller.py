import json

from app.api.base.controller import BaseController
from app.api.base.schema import ResponseData
from app.api.v1.endpoints.approval_v2.template.amount_block_TMS.schema import (
    TMSAccountAmountBlockResponse
)
from app.api.v1.endpoints.approval_v2.template.amount_unblock_template.schema import (
    TMSAccountAmountUnblockRequest
)
from app.api.v1.endpoints.approval_v2.template.repository import (
    repo_form, repos_check_exist_and_get_info_template_booking,
    repos_get_all_template_of_booking, repos_get_template_data
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    TMSCasaTopUpResponse
)
from app.api.v1.endpoints.approval_v2.template.transfer_TMS.schema import (
    TMSCasaTransferResponse
)
from app.api.v1.endpoints.approval_v2.template.withdraw.schema import (
    TMSWithdrawResponse
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CASA_TOP_UP, BUSINESS_TYPE_CASA_TRANSFER,
    BUSINESS_TYPE_WITHDRAW
)


class CtrTemplateDetail(BaseController):
    async def ctr_get_template_detail(self, template_id: str, booking_id: str):
        template_booking_info = self.call_repos(
            await repos_check_exist_and_get_info_template_booking(template_id, booking_id, session=self.oracle_session)
        )

        business_form_id__data = self.call_repos(
            await repos_get_template_data(
                booking=template_booking_info['booking_info'],
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

        elif object_data['business_type_id'] == BUSINESS_TYPE_WITHDRAW:
            object_data = ResponseData[TMSWithdrawResponse](**self.response(data=object_data))

        elif object_data['business_type_id'] == BUSINESS_TYPE_AMOUNT_UNBLOCK:
            # for account_unlock in object_data['account_unlock']:
            #     if account_unlock['account_amount_block']['p_type_unblock'] == 'C':
            #         account_unlock['account_amount_block']['checkbox_value'] = 'Toàn bộ số tiền tạm khóa'
            #     else:
            #         account_unlock['account_amount_block']['checkbox_value'] = 'Một phần số tiền tạm khóa, số tiền:'

            object_data = ResponseData[TMSAccountAmountUnblockRequest](**self.response(data=object_data))

        elif object_data['business_type_id'] == BUSINESS_TYPE_AMOUNT_BLOCK:
            object_data = ResponseData[TMSAccountAmountBlockResponse](**self.response(data=object_data))

        elif object_data['business_type_id'] == BUSINESS_TYPE_CASA_TRANSFER:
            object_data = ResponseData[TMSCasaTransferResponse](**self.response(data=object_data))

        return object_data

    async def ctr_get_template_after_fill(self, booking_id: str):
        template_booking_info = self.call_repos(
            await repos_check_exist_and_get_info_template_booking(template_id=None, booking_id=booking_id, session=self.oracle_session)
        )

        all_template_of_booking = self.call_repos(
            await repos_get_all_template_of_booking(
                template_booking_info['booking_info'].business_type_id,
                session=self.oracle_session)
        )

        template_ids = [template.id for template in all_template_of_booking]  # noqa
        data_return = {  # noqa
            'folder_name': all_template_of_booking[0].BusinessType.name,
            'templates': []
        }
        for template in all_template_of_booking:
            template_after_fill = self.call_repos(  # noqa
                await repo_form(template_id=template.template_id, booking_id=booking_id, path=template.template_url)
            )

        return self.response(None)
