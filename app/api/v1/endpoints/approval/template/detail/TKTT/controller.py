from app.api.base.controller import BaseController
from app.utils.constant.tms_dms import (
    TKTT_AMOUNT_BLOCK_TEMPLATE_5183, TKTT_AMOUNT_BLOCK_TEMPLATE_5184,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5185, TKTT_AMOUNT_BLOCK_TEMPLATE_5186,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5187, TKTT_AMOUNT_BLOCK_TEMPLATE_5188,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5189, TKTT_AMOUNT_BLOCK_TEMPLATE_5190,
    TKTT_AMOUNT_BLOCK_TEMPLATES, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5175,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5176, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5177,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5178, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5179,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5180, TKTT_AMOUNT_UNBLOCK_TEMPLATES,
    TKTT_TOP_UP_TEMPLATE_5181, TKTT_TOP_UP_TEMPLATE_5182, TKTT_TOP_UP_TEMPLATES
)


class CtrTemplateDetailTKTT(BaseController):

    async def ctr_get_template_detail_amount_unblock(self, template_id, booking_id):
        template = None

        if template_id not in TKTT_AMOUNT_UNBLOCK_TEMPLATES:
            return self.response_exception(msg='template_id not exist in amount unblock',
                                           detail=f'template_id: {template_id}')
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5175:
            template = await self.ctr_tktk_amount_unblock_form_5175(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5176:
            template = await self.ctr_tktk_amount_unblock_form_5176(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5177:
            template = await self.ctr_tktk_amount_unblock_form_5177(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5178:
            template = await self.ctr_tktk_amount_unblock_form_5178(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5179:
            template = await self.ctr_tktk_amount_unblock_form_5179(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5180:
            template = await self.ctr_tktk_amount_unblock_form_5180(booking_id=booking_id)

        return self.response(template)

    async def ctr_tktk_amount_unblock_form_5175(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5176(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5177(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5178(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5179(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5180(self, booking_id: str):
        pass

    async def ctr_get_template_detail_top_up(self, template_id, booking_id):
        template = None

        if template_id not in TKTT_TOP_UP_TEMPLATES:
            return self.response_exception(msg='template_id not exist in casa top up',
                                           detail=f'template_id: {template_id}')

        if template_id == TKTT_TOP_UP_TEMPLATE_5181:
            template = await self.ctr_tktk_top_up_form_5181(booking_id=booking_id)
        if template_id == TKTT_TOP_UP_TEMPLATE_5182:
            template = await self.ctr_tktk_top_up_form_5182(booking_id=booking_id)

        return self.response(template)

    async def ctr_tktk_top_up_form_5181(self, template_id, booking_id: str):
        pass

    async def ctr_tktk_top_up_form_5182(self, booking_id: str):
        pass

    async def ctr_get_template_detail_amount_block(self, template_id, booking_id):

        template = None
        if template_id not in TKTT_AMOUNT_BLOCK_TEMPLATES:
            return self.response_exception(msg='template_id not exist in amount block',
                                           detail=f'template_id: {template_id}')
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5183:
            template = await self.ctr_tktk_amount_block_form_5183(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5184:
            template = await self.ctr_tktk_amount_block_form_5184(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5185:
            template = await self.ctr_tktk_amount_block_form_5185(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5186:
            template = await self.ctr_tktk_amount_block_form_5186(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5187:
            template = await self.ctr_tktk_amount_block_form_5187(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5188:
            template = await self.ctr_tktk_amount_block_form_5188(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5189:
            template = await self.ctr_tktk_amount_block_form_5189(booking_id=booking_id)
        if template_id == TKTT_AMOUNT_BLOCK_TEMPLATE_5190:
            template = await self.ctr_tktk_amount_block_form_5190(booking_id=booking_id)

        return self.response(template)

    async def ctr_tktk_amount_block_form_5183(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5184(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5185(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5186(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5187(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5188(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5189(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5190(self, booking_id: str):
        pass
