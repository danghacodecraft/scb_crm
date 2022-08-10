from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.approval.template.detail.repository import (
    repo_form, repos_branch_name
)
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
from app.api.v1.others.booking.repository import repos_get_booking
from app.api.v1.others.statement.controller import CtrStatement
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_CASA_TOP_UP
)
from app.utils.constant.casa import (
    RECEIVING_METHOD_ACCOUNT_CASES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.date_datetime import DATE_TYPE_DMY_WITH_SLASH
from app.utils.constant.gw import (
    GW_DATETIME_FORMAT, GW_FUNC_AMOUNT_UNBLOCK_OUT
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
    TKTT_PATH_FORM_5175, TKTT_PATH_FORM_5178, TKTT_PATH_FORM_5181,
    TKTT_PATH_FORM_5182, TKTT_PATH_FORM_5183, TKTT_PATH_FORM_5184,
    TKTT_PATH_FORM_5187, TKTT_TOP_UP_TEMPLATE_5181, TKTT_TOP_UP_TEMPLATE_5182,
    TKTT_TOP_UP_TEMPLATES
)
from app.utils.error_messages import ERROR_BOOKING_INCORRECT
from app.utils.functions import (
    date_string_to_other_date_string_format, date_to_string, now, orjson_loads
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
        if template_id == TKTT_AMOUNT_UNBLOCK_TEMPLATE_5180:
            template = await self.ctr_tktk_amount_unblock_form_5180(booking_id=booking_id)

        return template

    async def ctr_tktk_amount_unblock_form_5175(self, booking_id: str):
        """
        Biểu mẫu 5175
        """
        data_request = {}
        current_user = self.current_user
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_TYPE_AMOUNT_UNBLOCK,
                session=self.oracle_session

            ))

        # Thông tin phiếu thu
        request_data_gw = orjson_loads(booking_business_form.form_data)
        supervisor_info = request_data_gw['staff_info_checker']['staff_name']
        employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
            employee_name=supervisor_info
        )
        supervisor = employee_info['data']['fullname_vn']
        log_data = orjson_loads(booking_business_form.log_data)
        branch_name = log_data[GW_FUNC_AMOUNT_UNBLOCK_OUT]['transaction_info']['branch_info']['branch_name']

        data_request.update(
            {
                "S1.A.1.12.1": branch_name,
                "S1.A.1.12.2": 'Lê Quang Anh',   # TODO
                "S1.A.1.12.3": '189785456',      # TODO
                "S1.A.1.12.4": '20/01/2010',     # TODO
                "S1.A.1.12.5": 'Tp.Hồ Chí Minh',     # TODO
                "S1.A.1.12.7": branch_name,     # TODO
                "S1.A.1.12.8": '123456789888',     # TODO
                "S1.A.1.12.9": '20/07/2020',     # TODO
                # "S1.A.1.12.10": 'True',     # TODO
                "S1.A.1.12.11": 'True',     # TODO
                "S1.A.1.12.12": '<50000000> <100000000>',     # TODO
                "S1.A.1.12.13": 'Năm mươi triệu',     # TODO
                "S1.A.1.12.14": str(now().strftime("%d")),
                "S1.A.1.12.15": str(now().strftime("%m")),
                "S1.A.1.12.16": str(now().strftime("%Y")),
                "S1.A.1.12.17": str(now().strftime("%d")),
                "S1.A.1.12.18": current_user.user_info.name,
                "S1.A.1.12.19": supervisor if not supervisor else ''
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5175))
        return data_tms
        # return data_request

    async def ctr_tktk_amount_unblock_form_5176(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5177(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5178(self, booking_id: str):
        """
        Biểu mẫu 5178
        """
        data_request = {}
        current_user = self.current_user
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=booking_id,
                business_form_id=BUSINESS_TYPE_AMOUNT_UNBLOCK,
                session=self.oracle_session

            ))

        # Thông tin phiếu thu
        request_data_gw = orjson_loads(booking_business_form.form_data)
        supervisor_info = request_data_gw['staff_info_checker']['staff_name']
        employee_info = await CtrGWEmployee(current_user).ctr_gw_get_employee_info_from_user_name(
            employee_name=supervisor_info
        )
        supervisor = employee_info['data']['fullname_vn']
        log_data = orjson_loads(booking_business_form.log_data)
        branch_name = log_data[GW_FUNC_AMOUNT_UNBLOCK_OUT]['transaction_info']['branch_info']['branch_name']

        data_request.update(
            {
                "S1.A.1.12.1": branch_name,
                "S1.A.1.12.2": 'Lê Quang Anh',   # TODO
                "S1.A.1.12.3": '189785456',      # TODO
                "S1.A.1.12.4": '20/01/2010',     # TODO
                "S1.A.1.12.5": 'Tp.Hồ Chí Minh',     # TODO
                "S1.A.1.12.6": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',     # TODO
                "S1.A.1.12.7": branch_name,     # TODO
                "S1.A.1.12.8": '123456789888',     # TODO
                "S1.A.1.12.9": '20/07/2020',     # TODO
                "S1.A.1.12.10": 'True',     # TODO
                "S1.A.1.12.11": '50000000',     # TODO
                "S1.A.1.12.12": '50000000',     # TODO
                "S1.A.1.12.13": 'Năm mươi triệu',     # TODO
                "S1.A.1.12.14": str(now().strftime("%d")),
                "S1.A.1.12.15": str(now().strftime("%m")),
                "S1.A.1.12.16": str(now().strftime("%Y")),
                "S1.A.1.12.17": str(now().strftime("%d/%m/%Y")),
                "S1.A.1.12.18": current_user.user_info.name,
                "S1.A.1.12.19": supervisor if not supervisor else ''
            }
        )

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5178))
        return data_tms

    async def ctr_tktk_amount_unblock_form_5179(self, booking_id: str):
        pass

    async def ctr_tktk_amount_unblock_form_5180(self, booking_id: str):
        pass

    async def ctr_get_template_detail_top_up(self, template_id, booking_id):
        template = None
        current_user = self.current_user

        if template_id not in TKTT_TOP_UP_TEMPLATES:
            return self.response_exception(msg='template_id not exist in casa top up',
                                           detail=f'template_id: {template_id}')

        if template_id == TKTT_TOP_UP_TEMPLATE_5181:
            template = await self.ctr_tktk_top_up_form_5181(booking_id=booking_id, current_user=current_user)
        if template_id == TKTT_TOP_UP_TEMPLATE_5182:
            template = await self.ctr_tktk_top_up_form_5182(booking_id=booking_id, current_user=current_user)

        return template

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
                receiver_full_name_vn = "abc"  # TODO

        elif receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            receiver_full_name_vn = "abc"  # TODO
        else:
            if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

        statement = await CtrStatement(current_user).ctr_statement_info(statement_request=form_data['statement'])
        data_request.update({
            "S1.A.1.3.3": log_data['branch_name'],
            "S1.A.1.3.4": date_string_to_other_date_string_format(
                log_data['created_at'], from_format=GW_DATETIME_FORMAT, to_format=DATE_TYPE_DMY_WITH_SLASH),
            "S1.A.1.3.1": "",  # TODO số chứng từ
            "S1.A.1.3.2": date_string_to_other_date_string_format(
                log_data['completed_at'], from_format=GW_DATETIME_FORMAT, to_format=DATE_TYPE_DMY_WITH_SLASH),
            "S1.A.1.3.5": log_data['user_id'],

            "S1.A.1.3.6": form_data['receiver_account_number'] if 'receiver_account_number' in form_data.keys() else '',

            'S1.A.1.3.7': "VND",  # TODO đơn vị tính
            "S1.A.1.3.8": receiver_full_name_vn,
            "S1.A.1.3.12": "",  # TODO sản phẩm
            "S1.A.1.3.13": str(actual_total),
            "S1.A.1.3.14": str(fee_amount),
            "S1.A.1.3.15": str(vat_tax),
            "S1.A.1.3.16": str(actual_total),
            "S1.A.1.3.17": form_data['content'] if 'content' in form_data.keys() else '',
            'S1.A.1.3.18': form_data['sender_full_name_vn'] if 'sender_full_name_vn' in form_data.keys() else '',
            'S1.A.1.3.19': form_data['sender_mobile_number'] if 'sender_mobile_number' in form_data.keys() else '',
            'S1.A.1.3.20': form_data['sender_identity_number'] if 'sender_identity_number' in form_data.keys() else '',
            'S1.A.1.3.21': form_data['sender_issued_date'] if 'sender_issued_date' in form_data.keys() else '',
            'S1.A.1.3.22': place_of_issue_name,
            'S1.A.1.3.23': form_data['sender_address_full'] if 'sender_address_full' in form_data.keys() else '',

            'S1.A.1.3.26': maker_name,
            'S1.A.1.3.27': current_user.user_info.name,

            'S1.A.1.3.24': str(statement['total_number_of_bills']),
            'S1.A.1.3.25': str(statement['total']),

            'S1.A.1.3.9': [
                {
                    'S1.A.1.3.9': str(statement_item['denominations']),
                    'S1.A.1.3.10': str(statement_item['amount']),
                    'S1.A.1.3.11': str(statement_item['into_money'])
                } for statement_item in statement['statements']
            ]
        })

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5181)
        )

        return data_tms

    async def ctr_tktk_top_up_form_5182(self, booking_id: str, current_user: AuthResponse):
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
                receiver_full_name_vn = "abc"  # TODO

        elif receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD:
            receiver_full_name_vn = "abc"  # TODO
        else:
            if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

            if receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
                receiver_full_name_vn = form_data['receiver_full_name_vn']

        statement = await CtrStatement(current_user).ctr_statement_info(statement_request=form_data['statement'])
        data_request.update({
            "S1.A.1.3.3": log_data['branch_name'],
            "S1.A.1.3.4": date_string_to_other_date_string_format(
                log_data['created_at'], from_format=GW_DATETIME_FORMAT, to_format=DATE_TYPE_DMY_WITH_SLASH),
            "S1.A.1.3.1": "",  # TODO số chứng từ
            "S1.A.1.3.2": date_string_to_other_date_string_format(
                log_data['completed_at'], from_format=GW_DATETIME_FORMAT, to_format=DATE_TYPE_DMY_WITH_SLASH),
            "S1.A.1.3.5": log_data['user_id'],

            "S1.A.1.3.6": form_data['receiver_account_number'] if 'receiver_account_number' in form_data.keys() else '',

            'S1.A.1.3.7': "VND",  # TODO hard code đơn vị tính
            "S1.A.1.3.8": receiver_full_name_vn,
            "S1.A.1.3.12": "",  # TODO sản phẩm
            "S1.A.1.3.13": str(actual_total),
            "S1.A.1.3.14": str(fee_amount),
            "S1.A.1.3.15": str(vat_tax),
            "S1.A.1.3.16": str(actual_total),
            "S1.A.1.3.17": form_data['content'] if 'content' in form_data.keys() else '',
            'S1.A.1.3.18': form_data['sender_full_name_vn'] if 'sender_full_name_vn' in form_data.keys() else '',
            'S1.A.1.3.19': form_data['sender_mobile_number'] if 'sender_mobile_number' in form_data.keys() else '',
            'S1.A.1.3.20': form_data['sender_identity_number'] if 'sender_identity_number' in form_data.keys() else '',
            'S1.A.1.3.21': form_data['sender_issued_date'] if 'sender_issued_date' in form_data.keys() else '',
            'S1.A.1.3.22': place_of_issue_name,
            'S1.A.1.3.23': form_data['sender_address_full'] if 'sender_address_full' in form_data.keys() else '',

            'S1.A.1.3.26': maker_name,
            'S1.A.1.3.27': current_user.user_info.name,

            'S1.A.1.3.24': str(statement['total_number_of_bills']),
            'S1.A.1.3.25': str(statement['total']),

            'S1.A.1.3.9': str(statement['statements'][0]['denominations']) if statement['statements'] else '',  # TODO
            'S1.A.1.3.10': str(statement['statements'][0]['amount']) if statement['statements'] else '',  # TODO
            'S1.A.1.3.11': str(statement['statements'][0]['into_money']) if statement['statements'] else ''  # TODO
        })

        data_tms = self.call_repos(
            await repo_form(data_request=data_request, path=TKTT_PATH_FORM_5182)
        )

        return data_tms

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
                "S1.A.1.5.1": 'Số chứng từ',  # TODO
                "S1.A.1.5.2": date_to_string(now()),
                "S1.A.1.5.3": branch_name,
                "S1.A.1.5.4": date_to_string(now()),
                "S1.A.1.5.5": current_user.user_info.code,
                "S1.A.1.5.6": request_data_gw['account_info']['account_num'],
                "S1.A.1.5.7": account_name['customer_info']['full_name'],
                "S1.A.1.5.8": 'VND',  # TODO
                "S1.A.1.5.9": '50000',  # TODO
                "S1.A.1.5.10": '10',                   # TODO
                "S1.A.1.5.11": '500000',               # TODO
                "S1.A.1.5.12": str(amount),
                "S1.A.1.5.13": '100000',               # TODO
                "S1.A.1.5.14": '10000',                # TODO
                "S1.A.1.5.15": str(amount),
                "S1.A.1.5.16": 'Phong tỏa tài khoản',  # TODO
                "S1.A.1.5.17": 'Đặng Thị Hồng Hà',     # TODO
                "S1.A.1.5.18": '0989868686',           # TODO
                "S1.A.1.5.19": '1999',                 # TODO
                "S1.A.1.5.20": '20/01/2020',           # TODO
                "S1.A.1.5.21": 'Tp. Hồ Chí Minh',      # TODO
                "S1.A.1.5.22": '927 Trần Hưng Đạo Phường 1 Quận 5 Tp.HCM',     # TODO
                "S1.A.1.5.23": '10',                   # TODO
                "S1.A.1.5.24": '500000',               # TODO
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
            "S1.A.1.11.3": '175896586',         # TODO
            "S1.A.1.11.4": '20/11/2010',         # TODO
            "S1.A.1.11.5": 'Hồ Chí Minh',         # TODO
            "S1.A.1.11.6": branch_name,
            "S1.A.1.11.7": account_no,
            "S1.A.1.11.8": str(open_date),
            "S1.A.1.11.9": balance,
            "S1.A.1.11.10": str(amount_locked),
            "S1.A.1.11.11": '500000000',
            "S1.A.1.11.12": 'Năm trăm triệu',
            "S1.A.1.11.13": str(effective_date),
            "S1.A.1.11.14": str(expiry_date),
            "S1.A.1.11.15": reasons,
            # "S1.A.1.11.16": ['Trích tiền từ tài khoản thanh toán'],  # TODO
            "S1.A.1.11.16": ['Nộp tiền mặt /In cash'],  # TODO
            "S1.A.1.11.18": '123456789',     # TODO
            "S1.A.1.11.19": 'DANG THI HA',      # TODO
            "S1.A.1.11.20": str(now().strftime("%d")),
            "S1.A.1.11.21": str(now().strftime("%m")),
            "S1.A.1.11.22": str(now().strftime("%Y")),
            "S1.A.1.11.28": str(now().strftime("%H:%M")),
            "S1.A.1.11.29": str(date_to_string(now())),
            "S1.A.1.11.30": "500000",     # TODO
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
                "S1.A.1.5.15": str(amount),
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
