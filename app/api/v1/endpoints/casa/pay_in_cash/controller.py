from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import (
    repos_get_customer_by_cif_number
)
from app.api.v1.endpoints.casa.pay_in_cash.repository import (
    repos_get_pay_in_cash_info, repos_save_pay_in_cash_info
)
from app.api.v1.endpoints.casa.pay_in_cash.schema import (
    PayInCashSCBByIdentity, PayInCashSCBToAccountRequest,
    PayInCashThirdParty247ToAccount, PayInCashThirdParty247ToCard,
    PayInCashThirdPartyByIdentity, PayInCashThirdPartyToAccount
)
from app.api.v1.endpoints.repository import repos_get_branch_in_province
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.employee.controller import (
    CtrGWEmployee
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.third_parties.oracle.models.master_data.address import AddressProvince
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.approval import PAY_IN_CASH_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_PAY_IN_CASH
from app.utils.constant.casa import (
    DENOMINATIONS__AMOUNTS, RECEIVING_METHOD__METHOD_TYPES,
    RECEIVING_METHOD_IDENTITY_CASES, RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_SCB_TO_ACCOUNT, RECEIVING_METHODS
)
from app.utils.constant.gw import GW_REQUEST_DIRECT_INDIRECT
from app.utils.constant.idm import (
    IDM_GROUP_ROLE_CODE_GDV, IDM_MENU_CODE_TTKH, IDM_PERMISSION_CODE_GDV
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_NUMBER_NOT_EXIST,
    ERROR_DENOMINATIONS_NOT_EXIST, ERROR_NOT_NULL,
    ERROR_RECEIVING_METHOD_NOT_EXIST, USER_CODE_NOT_EXIST
)
from app.utils.functions import dropdown, orjson_loads


class CtrPayInCash(BaseController):
    async def ctr_get_pay_in_cash_info(self, booking_id: str):
        current_user = self.current_user
        get_pay_in_cash_info = self.call_repos(await repos_get_pay_in_cash_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_pay_in_cash_info.form_data)
        receiving_method = form_data['receiving_method']

        ################################################################################################################
        # Thông tin người thụ hưởng
        ################################################################################################################
        receiver_response = {}

        if receiving_method not in RECEIVING_METHOD_IDENTITY_CASES:
            account_number = form_data['account_number']

            gw_casa_account_info = await CtrGWCasaAccount(current_user=current_user).ctr_gw_get_casa_account_info(
                account_number=account_number,
                return_raw_data_flag=True
            )

            gw_casa_account_info_customer_info = gw_casa_account_info['customer_info']
            account_info = gw_casa_account_info_customer_info['account_info']

            receiver_response = dict(
                account_number=account_number,
                fullname_vn=gw_casa_account_info_customer_info['full_name'],
                currency=account_info['account_currency'],
                branch_info=dict(
                    id=account_info['branch_info']['branch_code'],
                    code=account_info['branch_info']['branch_code'],
                    name=account_info['branch_info']['branch_name']
                )
            )
        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            province = await self.get_model_object_by_id(
                model_id=form_data['province']['id'], model=AddressProvince, loc='province_id'
            )
            branch_info = await self.get_model_object_by_id(
                model_id=form_data['branch']['id'], model=Branch, loc='branch_id'
            )
            place_of_issue = await self.get_model_object_by_id(
                model_id=form_data['place_of_issue']['id'], model=PlaceOfIssue, loc='place_of_issue_id'
            )
            receiver_response = dict(
                province=dropdown(province),
                branch_info=dropdown(branch_info),
                fullname_vn=form_data['full_name_vn'],
                identity_number=form_data['identity_number'],
                issued_date=form_data['issued_date'],
                place_of_issue=dropdown(place_of_issue),
                mobile_number=form_data['mobile_number'],
                address_full=form_data['address_full']
            )
        ################################################################################################################

        amount = form_data['amount']

        ################################################################################################################
        # Thông tin phí
        ################################################################################################################
        fee_info = form_data['fee_info']
        fee_amount = fee_info['fee_amount']
        vat_tax = fee_amount / 10
        total = fee_amount + vat_tax
        actual_total = total + amount
        is_transfer_payer = False
        payer = None
        if fee_info['is_transfer_payer'] is not None:
            payer = "RECEIVER"
            if fee_info['is_transfer_payer'] is True:
                is_transfer_payer = True
                payer = "SENDER"

        fee_info.update(dict(
            vat_tax=vat_tax,
            total=total,
            actual_total=actual_total,
            is_transfer_payer=is_transfer_payer,
            payer=payer
        ))
        ################################################################################################################

        ################################################################################################################
        # Bảng kê
        ################################################################################################################
        statement = DENOMINATIONS__AMOUNTS
        for row in form_data['statement']:
            statement.update({row['denominations']: row['amount']})

        statements = []
        total_amount = 0
        for denominations, amount in statement.items():
            into_money = int(denominations) * amount
            statements.append(dict(
                denominations=denominations,
                amount=amount,
                into_money=into_money
            ))
            total_amount += into_money
        statement_response = dict(
            statements=statements,
            total=total_amount,
            odd_difference=abs(actual_total - total_amount)
        )
        ################################################################################################################

        ################################################################################################################
        # Thông tin khách hàng giao dịch
        ################################################################################################################
        cif_number = form_data['cif_number']
        gw_customer_info = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
            cif_number=cif_number,
            return_raw_data_flag=True
        )
        gw_customer_info_identity_info = gw_customer_info['id_info']
        customer_response = dict(
            cif_number=cif_number,
            fullname_vn=gw_customer_info['full_name'],
            address_full=gw_customer_info['t_address_info']['contact_address_full'],
            identity_info=dict(
                number=gw_customer_info_identity_info['id_num'],
                issued_date=gw_customer_info_identity_info['id_issued_date'],
                place_of_issue=gw_customer_info_identity_info['id_issued_location']
            ),
            mobile_phone=gw_customer_info['mobile_phone'],
            telephone=gw_customer_info['telephone'],
            otherphone=gw_customer_info['otherphone']
        )
        controller_gw_employee = CtrGWEmployee(current_user)
        gw_direct_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['direct_staff_code'],
            return_raw_data_flag=True
        )
        direct_staff = dict(
            code=gw_direct_staff['staff_code'],
            name=gw_direct_staff['staff_name']
        )
        gw_indirect_staff = await controller_gw_employee.ctr_gw_get_employee_info_from_code(
            employee_code=form_data['indirect_staff_code'],
            return_raw_data_flag=True
        )
        indirect_staff = dict(
            code=gw_indirect_staff['staff_code'],
            name=gw_indirect_staff['staff_name']
        )
        ################################################################################################################

        response_data = dict(
            transfer_type=dict(
                receiving_method_type=RECEIVING_METHOD__METHOD_TYPES[receiving_method],
                receiving_method=receiving_method
            ),
            receiver=receiver_response,
            transfer=dict(
                amount=amount,
                content=form_data['content'],
                entry_number=None,  # TODO: Số bút toán
            ),
            fee_info=fee_info,
            statement=statement_response,
            customer=customer_response,
            direct_staff=direct_staff,
            indirect_staff=indirect_staff,
        )

        return self.response(response_data)

    async def ctr_save_pay_in_cash_scb_to_account(
            self,
            current_user: AuthResponse,
            request: PayInCashSCBToAccountRequest
    ):
        cif_number = request.cif_number
        if not cif_number:
            return self.response_exception(msg=ERROR_CIF_NUMBER_NOT_EXIST, loc=f"cif_number: {cif_number}")

        account_number = request.account_number

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=account_number
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f"account_number: {account_number}")

        return request

    async def ctr_save_pay_in_cash_scb_by_identity(
            self,
            request: PayInCashSCBByIdentity
    ):
        # validate province
        province_id = request.province.id
        await self.get_model_object_by_id(model_id=province_id, model=AddressProvince, loc='province -> id')

        # validate branch
        branch_id = request.branch.id
        self.call_repos(await repos_get_branch_in_province(
            branch_id=branch_id,
            province_id=province_id,
            session=self.oracle_session,
            loc=f'branch_id: {branch_id}, province_id: {province_id}'
        ))
        await self.get_model_object_by_id(model_id=branch_id, model=Branch, loc='branch -> id')

        # validate issued_date
        issued_date = request.issued_date
        await self.validate_issued_date(issued_date=issued_date, loc='issued_date')

        # validate place_of_issue
        place_of_issue_id = request.place_of_issue.id
        await self.get_model_object_by_id(model_id=place_of_issue_id, model=PlaceOfIssue, loc='place_of_issue -> id')

        return request

    async def ctr_save_pay_in_cash_info(
            self,
            booking_id: str,
            request: Union[
                PayInCashSCBToAccountRequest,
                PayInCashSCBByIdentity,
                PayInCashThirdPartyToAccount,
                PayInCashThirdPartyByIdentity,
                PayInCashThirdParty247ToAccount,
                PayInCashThirdParty247ToCard
            ]
    ):
        cif_number = request.cif_number
        receiving_method = request.receiving_method
        is_fee = request.is_fee
        fee_info = request.fee_info
        statement = request.statement
        direct_staff_code = request.direct_staff_code
        indirect_staff_code = request.indirect_staff_code
        current_user = self.current_user
        current_user_info = current_user.user_info
        ################################################################################################################
        # VALIDATE
        ################################################################################################################
        # check quyền user
        self.call_repos(await PermissionController().ctr_approval_check_permission(
            auth_response=current_user,
            menu_code=IDM_MENU_CODE_TTKH,
            group_role_code=IDM_GROUP_ROLE_CODE_GDV,
            permission_code=IDM_PERMISSION_CODE_GDV,
            stage_code=PAY_IN_CASH_STAGE_BEGIN
        ))

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_PAY_IN_CASH,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        if is_fee is not None and not fee_info:
            return self.response_exception(msg=ERROR_NOT_NULL, loc="fee_info")
            # TODO: Case cho bên chuyển/ Bên nhận

        denominations__amounts = DENOMINATIONS__AMOUNTS
        denominations_errors = []
        for index, row in enumerate(statement):
            denominations = row.denominations
            if denominations not in DENOMINATIONS__AMOUNTS:
                denominations_errors.append(dict(
                    index=index,
                    value=denominations
                ))

            denominations__amounts[denominations] = row.amount

        if denominations_errors:
            return self.response_exception(
                msg=ERROR_DENOMINATIONS_NOT_EXIST,
                loc=str(denominations_errors)
            )

        if direct_staff_code:
            gw_direct_staffs = await CtrSelectCategory(current_user).ctr_select_category(
                transaction_name=GW_REQUEST_DIRECT_INDIRECT,
                transaction_value=[
                    {
                        "param1": "D",
                        "param2": current_user_info.hrm_branch_code
                    }
                ]
            )
            is_direct_staff = False
            for gw_direct_staff in gw_direct_staffs['data']:
                if direct_staff_code == gw_direct_staff['employee_code']:
                    is_direct_staff = True
                    break
            if not is_direct_staff:
                return self.response_exception(msg=USER_CODE_NOT_EXIST, loc=f'direct_staff_code: {direct_staff_code}')

        if indirect_staff_code:
            gw_indirect_staffs = await CtrSelectCategory(current_user).ctr_select_category(
                transaction_name=GW_REQUEST_DIRECT_INDIRECT,
                transaction_value=[
                    {
                        "param1": "I",
                        "param2": current_user_info.hrm_branch_code
                    }
                ]
            )
            is_indirect_staff = False
            for gw_indirect_staff in gw_indirect_staffs['data']:
                if indirect_staff_code == gw_indirect_staff['employee_code']:
                    is_indirect_staff = True
                    break
            if not is_indirect_staff:
                return self.response_exception(
                    msg=USER_CODE_NOT_EXIST, loc=f'indirect_staff_code: {indirect_staff_code}'
                )

        # Kiểm tra số CIF có tồn tại trong CRM không
        if cif_number:
            self.call_repos(await repos_get_customer_by_cif_number(
                cif_number=cif_number,
                session=self.oracle_session
            ))

        if receiving_method not in RECEIVING_METHODS:
            return self.response_exception(
                msg=ERROR_RECEIVING_METHOD_NOT_EXIST,
                loc=f'receiving_method: {receiving_method}'
            )
        ################################################################################################################

        pay_in_cash_info = None
        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            pay_in_cash_info = await self.ctr_save_pay_in_cash_scb_to_account(
                current_user=current_user,
                request=request
            )
        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY:
            pay_in_cash_info = await self.ctr_save_pay_in_cash_scb_by_identity(request=request)

        self.call_repos(await repos_save_pay_in_cash_info(
            booking_id=booking_id,
            form_data=pay_in_cash_info.json(),
            session=self.oracle_session
        ))

        return self.response(data=pay_in_cash_info)
