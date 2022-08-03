from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.detail.repository import repo_form
from app.api.v1.endpoints.casa.top_up.repository import (
    repos_get_casa_top_up_info
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TOP_UP
from app.utils.constant.tms_dms import (
    TKTT_AMOUNT_BLOCK_TEMPLATE_5183, TKTT_AMOUNT_BLOCK_TEMPLATE_5184,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5185, TKTT_AMOUNT_BLOCK_TEMPLATE_5186,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5187, TKTT_AMOUNT_BLOCK_TEMPLATE_5188,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5189, TKTT_AMOUNT_BLOCK_TEMPLATE_5190,
    TKTT_AMOUNT_BLOCK_TEMPLATES, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5175,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5176, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5177,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5178, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5179,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5180, TKTT_AMOUNT_UNBLOCK_TEMPLATES,
    TKTT_PATH_FORM_5181, TKTT_TOP_UP_TEMPLATE_5181, TKTT_TOP_UP_TEMPLATE_5182,
    TKTT_TOP_UP_TEMPLATES
)
from app.utils.error_messages import ERROR_BOOKING_INCORRECT
from app.utils.functions import orjson_loads


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

    async def ctr_tktk_top_up_form_5181(self, booking_id: str):
        data_request = {}

        booking = await CtrBooking().ctr_get_booking(booking_id=booking_id,
                                                     business_type_code=BUSINESS_TYPE_CASA_TOP_UP)
        if booking.business_type.id != BUSINESS_TYPE_CASA_TOP_UP:
            return self.response_exception(
                msg=ERROR_BOOKING_INCORRECT, loc=f"business_type: {booking.business_type.id}"
            )

        get_casa_top_up_info = self.call_repos(await repos_get_casa_top_up_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_casa_top_up_info.form_data)
        log_data = orjson_loads(get_casa_top_up_info.log_data)[0]

        transfer_amount = form_data['amount']

        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
        fee_info = form_data['fee_info']
        fee_amount = fee_info['fee_amount']
        vat_tax = int(fee_amount / 10)
        total = fee_amount + vat_tax
        actual_total = total + transfer_amount

        data_request.update({
            "S1.A.1.3.3": log_data['branch_name'],
            "S1.A.1.3.4": log_data['created_at'],
            "S1.A.1.3.1": "",  # TODO số chứng từ
            "S1.A.1.3.2": log_data['completed_at'],
            "S1.A.1.3.5": log_data['user_id'],

            "S1.A.1.3.6": form_data['receiver_account_number'] if 'receiver_account_number' in form_data.keys() else '',
            "S1.A.1.3.8": '',
            "S1.A.1.3.12": "",  # TODO sản phẩm
            "S1.A.1.3.13": actual_total,
            "S1.A.1.3.14": fee_amount,
            "S1.A.1.3.15": vat_tax,
            "S1.A.1.3.16": "",  # TODO số tiền bằng chữ
            "S1.A.1.3.17": form_data['content'] if 'content' in form_data.keys() else '',
            'S1.A.1.3.18': form_data['sender_full_name_vn'] if 'sender_full_name_vn' in form_data.keys() else '',
            'S1.A.1.3.19': form_data['sender_mobile_number'] if 'sender_mobile_number' in form_data.keys() else '',
            'S1.A.1.3.20': form_data['sender_identity_number'] if 'sender_identity_number' in form_data.keys() else '',
            'S1.A.1.3.21': form_data['sender_issued_date'] if 'sender_issued_date' in form_data.keys() else '',
            'S1.A.1.3.22': form_data['sender_place_of_issue']['id'] if 'sender_place_of_issue' in form_data.keys() else '',
            'S1.A.1.3.23': form_data['sender_address_full'] if 'sender_address_full' in form_data.keys() else '',


            'S1.A.1.3.26': '',
            'S1.A.1.3.27': '',

        })

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5181)
        )

        return self.response(data_tms)

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
