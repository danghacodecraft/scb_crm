from num2words import num2words

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.detail.repository import repo_form
from app.api.v1.endpoints.casa.top_up.repository import (
    repos_get_casa_top_up_info
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.business_type import BUSINESS_TYPE_CASA_TOP_UP
from app.utils.constant.casa import (
    RECEIVING_METHOD_ACCOUNT_CASES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
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
        current_user = self.current_user
        template = None

        if template_id not in TKTT_TOP_UP_TEMPLATES:
            return self.response_exception(msg='template_id not exist in casa top up',
                                           detail=f'template_id: {template_id}')

        if template_id == TKTT_TOP_UP_TEMPLATE_5181:
            template = await self.ctr_tktk_top_up_form_5181(booking_id=booking_id, current_user=current_user)
        if template_id == TKTT_TOP_UP_TEMPLATE_5182:
            template = await self.ctr_tktk_top_up_form_5182(booking_id=booking_id, current_user=current_user)

        return self.response(template)

    async def ctr_tktk_top_up_form_5181(self, booking_id: str, current_user: AuthResponse):
        data_request = {}

        booking = await CtrBooking().ctr_get_booking(booking_id=booking_id,
                                                     business_type_code=BUSINESS_TYPE_CASA_TOP_UP)
        if booking.business_type.id != BUSINESS_TYPE_CASA_TOP_UP:
            return self.response_exception(
                msg=ERROR_BOOKING_INCORRECT, loc=f"business_type: {booking.business_type.id}"
            )

        maker = booking.created_by

        maker_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_code(
            employee_code=maker, return_raw_data_flag=True)

        maker_name = maker_info['full_name']

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
        if form_data['is_fee']:
            fee_info = form_data['fee_info']
            fee_amount = fee_info['fee_amount']
            vat_tax = int(fee_amount / 10)
            total = fee_amount + vat_tax
            actual_total = total + transfer_amount
        else:
            fee_amount = 0
            vat_tax = 0
            actual_total = transfer_amount

        sender_place_of_issue = form_data['sender_place_of_issue']
        place_of_issue_name = ""
        if form_data['sender_place_of_issue']:
            identity_place_of_issue = await self.get_model_object_by_id(
                model_id=sender_place_of_issue['id'],
                model=PlaceOfIssue,
                loc='sender_place_of_issue -> id'
            )
            place_of_issue_name = identity_place_of_issue.name

        receiving_method = form_data['receiving_method']
        receiver_full_name_vn = ""

        if receiving_method in RECEIVING_METHOD_ACCOUNT_CASES:
            receiver_account_number = form_data['receiver_account_number']

            if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
                gw_casa_account_info = await CtrGWCasaAccount(
                    current_user=current_user).ctr_gw_get_casa_account_info(
                    account_number=receiver_account_number,
                    return_raw_data_flag=True
                )

                gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']

                receiver_full_name_vn = gw_casa_account_info_customer_info['full_name']

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT:
                receiver_full_name_vn = "abc"

        elif receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            receiver_full_name_vn = "abc"
        else:
            if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

        data_request.update({
            "S1.A.1.3.3": log_data['branch_name'],
            "S1.A.1.3.4": log_data['created_at'],
            "S1.A.1.3.1": "",  # TODO số chứng từ
            "S1.A.1.3.2": log_data['completed_at'],
            "S1.A.1.3.5": log_data['user_id'],

            "S1.A.1.3.6": form_data['receiver_account_number'] if 'receiver_account_number' in form_data.keys() else '',
            "S1.A.1.3.8": receiver_full_name_vn,
            "S1.A.1.3.12": "",  # TODO sản phẩm
            "S1.A.1.3.13": str(actual_total),
            "S1.A.1.3.14": str(fee_amount),
            "S1.A.1.3.15": str(vat_tax),
            "S1.A.1.3.16": num2words(actual_total, lang='vi') + " đồng",
            "S1.A.1.3.17": form_data['content'] if 'content' in form_data.keys() else '',
            'S1.A.1.3.18': form_data['sender_full_name_vn'] if 'sender_full_name_vn' in form_data.keys() else '',
            'S1.A.1.3.19': form_data['sender_mobile_number'] if 'sender_mobile_number' in form_data.keys() else '',
            'S1.A.1.3.20': form_data['sender_identity_number'] if 'sender_identity_number' in form_data.keys() else '',
            'S1.A.1.3.21': form_data['sender_issued_date'] if 'sender_issued_date' in form_data.keys() else '',
            'S1.A.1.3.22': place_of_issue_name,
            'S1.A.1.3.23': form_data['sender_address_full'] if 'sender_address_full' in form_data.keys() else '',

            'S1.A.1.3.26': maker_name,
            'S1.A.1.3.27': current_user.user_info.name


        })

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5181)
        )

        return data_tms

    async def ctr_tktk_top_up_form_5182(self, booking_id: str, current_user: AuthResponse):
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
