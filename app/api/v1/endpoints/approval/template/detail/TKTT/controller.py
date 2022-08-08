# from num2words import num2words

from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.approval.template.detail.repository import (
    repo_form, repos_branch_name
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.others.booking.repository import repos_get_booking
from app.utils.constant.business_type import BUSINESS_TYPE_AMOUNT_BLOCK
from app.utils.constant.tms_dms import (
    TKTT_AMOUNT_BLOCK_TEMPLATE_5183, TKTT_AMOUNT_BLOCK_TEMPLATE_5184,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5185, TKTT_AMOUNT_BLOCK_TEMPLATE_5186,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5187, TKTT_AMOUNT_BLOCK_TEMPLATE_5188,
    TKTT_AMOUNT_BLOCK_TEMPLATE_5189, TKTT_AMOUNT_BLOCK_TEMPLATE_5190,
    TKTT_AMOUNT_BLOCK_TEMPLATES, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5175,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5176, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5177,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5178, TKTT_AMOUNT_UNBLOCK_TEMPLATE_5179,
    TKTT_AMOUNT_UNBLOCK_TEMPLATE_5180, TKTT_AMOUNT_UNBLOCK_TEMPLATES,
    TKTT_PATH_FORM_5183, TKTT_PATH_FORM_5184, TKTT_TOP_UP_TEMPLATE_5181,
    TKTT_TOP_UP_TEMPLATE_5182, TKTT_TOP_UP_TEMPLATES
)
from app.utils.functions import date_to_string, now, orjson_loads


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

        return template

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

        return template

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

        return template

    async def ctr_tktk_amount_block_form_5183(self, booking_id: str):
        """
        Biểu mẫu 5183
        """
        data_request = {}

        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_TYPE_AMOUNT_BLOCK,
                session=self.oracle_session

            ))

        booking_info = self.call_repos(await repos_get_booking(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            session=self.oracle_session
        ))

        branch_name = self.call_repos(await repos_branch_name(
            branch_id=booking_info.branch_id,
            session=self.oracle_session
        ))
        # Thông tin phiếu thu
        request_data_gw = orjson_loads(booking_business_form.form_data)
        account_name = await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_casa_account_info(
            account_number=request_data_gw['account_info']['account_num'],
            return_raw_data_flag=True
        )
        amount = request_data_gw['p_blk_detail']['AMOUNT']

        data_request.update(
            {
                "S1.A.1.5.1": 'Số chứng từ',  # Todo
                "S1.A.1.5.2": date_to_string(now()),
                "S1.A.1.5.3": branch_name,
                "S1.A.1.5.4": date_to_string(now()),
                "S1.A.1.5.5": str(booking_info.created_by) if booking_info.created_by else "",
                "S1.A.1.5.6": request_data_gw['account_info']['account_num'],
                "S1.A.1.5.7": account_name['customer_info']['full_name'],
                "S1.A.1.5.8": 'VND',  # Todo
                "S1.A.1.5.9": '50000',  # Todo
                "S1.A.1.5.10": '10',                   # Todo
                "S1.A.1.5.11": '500000',               # Todo
                "S1.A.1.5.12": str(amount),
                "S1.A.1.5.13": '100000',               # Todo
                "S1.A.1.5.14": '10000',                # Todo
                "S1.A.1.5.15": " đồng",
                # "S1.A.1.5.15": num2words(amount, lang='vi') + " đồng",
                "S1.A.1.5.16": 'Phong tỏa tài khoản',  # Todo
                "S1.A.1.5.17": 'Đặng Thị Hồng Hà',     # Todo
                "S1.A.1.5.18": '0989868686',           # Todo
                "S1.A.1.5.19": '1999',                 # Todo
                "S1.A.1.5.20": '20/01/2020',           # Todo
                "S1.A.1.5.21": 'Tp. Hồ Chí Minh',      # Todo
                "S1.A.1.5.22": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',     # Todo
                "S1.A.1.5.23": '10',                   # Todo
                "S1.A.1.5.24": '500000',               # Todo
                "S1.A.1.5.25": 'Đặng Thị Hồng Hà',     # Todo
                "S1.A.1.5.26": 'Nguyễn Hồng Ánh',      # Todo
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5183))
        return data_tms

    async def ctr_tktk_amount_block_form_5184(self, booking_id: str):
        """
        Biểu mẫu 5184
        """
        data_request = {}

        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_TYPE_AMOUNT_BLOCK,
                session=self.oracle_session

            ))

        booking_info = self.call_repos(await repos_get_booking(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            session=self.oracle_session
        ))

        branch_name = self.call_repos(await repos_branch_name(
            branch_id=booking_info.branch_id,
            session=self.oracle_session
        ))
        # Thông tin phiếu thu
        request_data_gw = orjson_loads(booking_business_form.form_data)
        account_name = await CtrGWCasaAccount(current_user=self.current_user).ctr_gw_get_casa_account_info(
            account_number=request_data_gw['account_info']['account_num'],
            return_raw_data_flag=True
        )
        amount = request_data_gw['p_blk_detail']['AMOUNT']

        data_request.update(
            {
                "S1.A.1.5.1": 'Số chứng từ',  # Todo
                "S1.A.1.5.2": date_to_string(now()),
                "S1.A.1.5.3": branch_name,
                "S1.A.1.5.4": date_to_string(now()),
                "S1.A.1.5.5": str(booking_info.created_by) if booking_info.created_by else "",
                "S1.A.1.5.6": request_data_gw['account_info']['account_num'],
                "S1.A.1.5.7": account_name['customer_info']['full_name'],
                "S1.A.1.5.8": 'VND',  # Todo
                "S1.A.1.5.9": '50000',  # Todo
                "S1.A.1.5.10": '10',  # Todo
                "S1.A.1.5.11": '500000',  # Todo
                "S1.A.1.5.12": str(amount),
                "S1.A.1.5.13": '100000',  # Todo
                "S1.A.1.5.14": '10000',  # Todo
                "S1.A.1.5.15": " đồng",
                # "S1.A.1.5.15": num2words(amount, lang='vi') + " đồng",
                "S1.A.1.5.16": 'Phong tỏa tài khoản',  # Todo
                "S1.A.1.5.17": 'Đặng Thị Hồng Hà',  # Todo
                "S1.A.1.5.18": '0989868686',  # Todo
                "S1.A.1.5.19": '1999',  # Todo
                "S1.A.1.5.20": '20/01/2020',  # Todo
                "S1.A.1.5.21": 'Tp. Hồ Chí Minh',  # Todo
                "S1.A.1.5.22": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',  # Todo
                "S1.A.1.5.23": '10',  # Todo
                "S1.A.1.5.24": '500000',  # Todo
                "S1.A.1.5.25": 'Đặng Thị Hồng Hà',  # Todo
                "S1.A.1.5.26": 'Nguyễn Hồng Ánh',  # Todo
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5184))
        return data_tms

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
