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
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
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
    TKTT_PATH_FORM_5183, TKTT_PATH_FORM_5184, TKTT_PATH_FORM_5187,
    TKTT_TOP_UP_TEMPLATE_5181, TKTT_TOP_UP_TEMPLATE_5182, TKTT_TOP_UP_TEMPLATES
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
        current_user = self.current_user
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
        supervisor_info = request_data_gw['staff_info_checker']['staff_name']
        employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
            employee_name=supervisor_info
        )
        supervisor = employee_info['data']['fullname_vn']

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
                "S1.A.1.5.5": current_user.user_info.code,
                "S1.A.1.5.6": request_data_gw['account_info']['account_num'],
                "S1.A.1.5.7": account_name['customer_info']['full_name'],
                "S1.A.1.5.8": 'VND',  # Todo
                "S1.A.1.5.9": '50000',  # Todo
                "S1.A.1.5.10": '10',                   # Todo
                "S1.A.1.5.11": '500000',               # Todo
                "S1.A.1.5.12": str(amount),
                "S1.A.1.5.13": '100000',               # Todo
                "S1.A.1.5.14": '10000',                # Todo
                "S1.A.1.5.15": amount,
                "S1.A.1.5.16": 'Phong tỏa tài khoản',  # Todo
                "S1.A.1.5.17": 'Đặng Thị Hồng Hà',     # Todo
                "S1.A.1.5.18": '0989868686',           # Todo
                "S1.A.1.5.19": '1999',                 # Todo
                "S1.A.1.5.20": '20/01/2020',           # Todo
                "S1.A.1.5.21": 'Tp. Hồ Chí Minh',      # Todo
                "S1.A.1.5.22": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',     # Todo
                "S1.A.1.5.23": '10',                   # Todo
                "S1.A.1.5.24": '500000',               # Todo
                "S1.A.1.5.25": current_user.user_info.name,
                "S1.A.1.5.26": supervisor if not supervisor else ''
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5183))
        return data_tms

    async def ctr_tktk_amount_block_form_5184(self, booking_id: str):
        """
        Biểu mẫu 5184
        """
        current_user = self.current_user
        data_request = {}
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_TYPE_AMOUNT_BLOCK,
                session=self.oracle_session

            ))
        request_data_gw = orjson_loads(booking_business_form.form_data)
        supervisor_info = request_data_gw['staff_info_checker']['staff_name']
        employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
            employee_name=supervisor_info
        )
        supervisor = employee_info['data']['fullname_vn']

        account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_info(
            account_number=request_data_gw['account_info']['account_num']
        )

        account_holder = account_info['data']['customer_info']['fullname_vn']
        account_no = account_info['data']['account_info']['number']
        open_date = account_info['data']['account_info']['open_date']
        balance = account_info['data']['account_info']['balance']
        amount_locked = request_data_gw['p_blk_detail']['AMOUNT']
        effective_date = request_data_gw['p_blk_detail']['EFFECTIVE_DATE']
        expiry_date = request_data_gw['p_blk_detail']['EXPIRY_DATE']
        reasons = request_data_gw['p_blk_detail']['HOLD_CODE']

        booking_info = self.call_repos(await repos_get_booking(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            session=self.oracle_session
        ))

        branch_name = self.call_repos(await repos_branch_name(
            branch_id=booking_info.branch_id,
            session=self.oracle_session
        ))

        data_request.update({
            "S1.A.1.11.1": branch_name,
            "S1.A.1.11.2": account_holder,
            "S1.A.1.11.3": '175896586',         # Todo
            "S1.A.1.11.4": '20/11/2010',         # Todo
            "S1.A.1.11.5": 'Hồ Chí Minh',         # Todo
            "S1.A.1.11.6": branch_name,
            "S1.A.1.11.7": account_no,
            "S1.A.1.11.8": str(open_date),
            "S1.A.1.11.9": balance,
            "S1.A.1.11.10": amount_locked,
            "S1.A.1.11.11": '500000000',
            "S1.A.1.11.12": 'Năm trăm triệu',
            "S1.A.1.11.13": str(effective_date),
            "S1.A.1.11.14": str(expiry_date),
            "S1.A.1.11.15": reasons,
            "S1.A.1.11.16": 'True',
            "S1.A.1.11.17": 'True',
            "S1.A.1.11.18": '123456789',
            "S1.A.1.11.19": 'DANG THI HA',
            "S1.A.1.11.20": str(now().strftime("%d")),
            "S1.A.1.11.21": str(now().strftime("%m")),
            "S1.A.1.11.22": str(now().strftime("%Y")),
            "S1.A.1.11.28": str(now().strftime("%H:%M")),
            "S1.A.1.11.29": str(date_to_string(now())),
            "S1.A.1.11.30": "500000",
            "S1.A.1.11.31": str(now().strftime("%H:%M")),
            "S1.A.1.11.32": str(date_to_string(now())),
            "S1.A.1.11.33": current_user.user_info.name,
            "S1.A.1.11.34": supervisor if not supervisor else '',
        })

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5184))
        return data_tms

    async def ctr_tktk_amount_block_form_5185(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5186(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5187(self, booking_id: str):
        """
        Biểu mẫu 5187
        """
        data_request = {}
        current_user = self.current_user
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
        supervisor_info = request_data_gw['staff_info_checker']['staff_name']
        employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
            employee_name=supervisor_info
        )
        supervisor = employee_info['data']['fullname_vn']

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
                "S1.A.1.5.5": current_user.user_info.code,
                "S1.A.1.5.6": request_data_gw['account_info']['account_num'],
                "S1.A.1.5.7": account_name['customer_info']['full_name'],
                "S1.A.1.5.8": 'VND',  # Todo
                "S1.A.1.5.9": '50000',  # Todo
                "S1.A.1.5.10": '10',  # Todo
                "S1.A.1.5.11": '500000',  # Todo
                "S1.A.1.5.12": str(amount),
                "S1.A.1.5.13": '100000',  # Todo
                "S1.A.1.5.14": '10000',  # Todo
                "S1.A.1.5.15": amount,
                "S1.A.1.5.16": 'Phong tỏa tài khoản',  # Todo
                "S1.A.1.5.17": 'Đặng Thị Hồng Hà',  # Todo
                "S1.A.1.5.18": '0989868686',  # Todo
                "S1.A.1.5.19": '1999',  # Todo
                "S1.A.1.5.20": '20/01/2020',  # Todo
                "S1.A.1.5.21": 'Tp. Hồ Chí Minh',  # Todo
                "S1.A.1.5.22": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',  # Todo
                "S1.A.1.5.23": '10',  # Todo
                "S1.A.1.5.24": '500000',  # Todo
                "S1.A.1.5.25": current_user.user_info.name,
                "S1.A.1.5.26": supervisor if supervisor else ""
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5187))
        return data_tms

    async def ctr_tktk_amount_block_form_5188(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5189(self, booking_id: str):
        pass

    async def ctr_tktk_amount_block_form_5190(self, booking_id: str):
        pass
