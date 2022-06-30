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
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.category.controller import (
    CtrSelectCategory
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_PAY_IN_CASH
from app.utils.constant.casa import (
    DENOMINATIONS__AMOUNTS, RECEIVING_METHOD__METHOD_TYPES,
    RECEIVING_METHOD_SCB_TO_ACCOUNT, RECEIVING_METHODS
)
from app.utils.constant.gw import GW_REQUEST_DIRECT_INDIRECT
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_DENOMINATIONS_NOT_EXIST,
    ERROR_NOT_NULL, ERROR_RECEIVING_METHOD_NOT_EXIST, USER_CODE_NOT_EXIST
)
from app.utils.functions import orjson_loads


class CtrPayInCash(BaseController):
    async def ctr_get_pay_in_cash_info(self, booking_id: str):
        current_user = self.current_user
        get_pay_in_cash_info = self.call_repos(await repos_get_pay_in_cash_info(
            booking_id=booking_id,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_pay_in_cash_info.form_data)
        account_number = form_data['account_number']

        gw_casa_account_info = await CtrGWCasaAccount(current_user=current_user).ctr_gw_get_casa_account_info(
            account_number=account_number
        )

        gw_casa_account_info = gw_casa_account_info['data']

        customer_info = gw_casa_account_info['customer_info']
        account_info = gw_casa_account_info['account_info']

        amount = form_data['amount']
        receiving_method = form_data['receiving_method']
        fee_info = form_data['fee_info']
        fee_amount = fee_info['fee_amount']
        vat_tax = fee_amount / 10
        total = fee_amount + vat_tax
        fee_info.update(dict(
            vat_tax=vat_tax,
            total=total,
            actual_total=total + amount
        ))
        response_data = dict(
            transfer_type=dict(
                receiving_method_type=RECEIVING_METHOD__METHOD_TYPES[receiving_method],
                receiving_method=receiving_method
            ),
            receiver=dict(
                account_number=account_number,
                fullname_vn=customer_info['fullname_vn'],
                branch_info=account_info['branch_info']
            ),
            transfer=dict(
                amount=amount,
                content=form_data['content'],
                entry_number=None,  # TODO: Số bút toán
            ),
            fee_info=fee_info
        )

        return self.response(response_data)

    async def ctr_save_pay_in_cash_scb_to_account(
            self,
            current_user: AuthResponse,
            request: PayInCashSCBToAccountRequest
    ):
        account_number = request.account_number

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=account_number
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(msg=ERROR_CASA_ACCOUNT_NOT_EXIST, loc=f"account_number: {account_number}")

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
        # self.call_repos(await PermissionController().ctr_approval_check_permission(
        #     auth_response=current_user,
        #     menu_code=IDM_MENU_CODE_OPEN_CIF,
        #     group_role_code=IDM_GROUP_ROLE_CODE_OPEN_CIF,
        #     permission_code=IDM_PERMISSION_CODE_OPEN_CIF,
        #     stage_code=PAY_IN_CASH_STAGE_BEGIN
        # ))

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_PAY_IN_CASH,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        if is_fee and not fee_info:
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

        self.call_repos(await repos_save_pay_in_cash_info(
            booking_id=booking_id,
            form_data=pay_in_cash_info.json(),
            session=self.oracle_session
        ))

        return self.response(data=pay_in_cash_info)
