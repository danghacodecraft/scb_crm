from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.detail.CIF.controller import (
    CtrTemplateDetailCIF
)
from app.api.v1.endpoints.approval.template.detail.TKTT.controller import (
    CtrTemplateDetailTKTT
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CASA_TOP_UP, BUSINESS_TYPE_INIT_CIF
)


class CtrTemplateDetail(BaseController):
    async def ctr_get_template_detail(self, template_id, booking_id):
        current_user = self.current_user
        business_type = await CtrBooking(current_user).ctr_get_business_type(booking_id=booking_id)
        business_type_id = business_type.id
        template = None
        if business_type_id == BUSINESS_TYPE_INIT_CIF:
            template = await CtrTemplateDetailCIF(current_user).ctr_get_template_detail_cif(
                booking_id=booking_id, template_id=template_id
            )

        if business_type_id == BUSINESS_TYPE_AMOUNT_UNBLOCK:
            template = await CtrTemplateDetailTKTT(current_user).ctr_get_template_detail_amount_unblock(
                booking_id=booking_id, template_id=template_id
            )

        if business_type_id == BUSINESS_TYPE_CASA_TOP_UP:
            template = await CtrTemplateDetailTKTT(current_user).ctr_get_template_detail_top_up(
                booking_id=booking_id, template_id=template_id
            )

        if business_type_id == BUSINESS_TYPE_AMOUNT_BLOCK:
            template = await CtrTemplateDetailTKTT(current_user).ctr_get_template_detail_amount_block(
                booking_id=booking_id, template_id=template_id
            )

        return self.response(template)
