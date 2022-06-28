from typing import Union

from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.open_casa.open_casa.repository import repos_get_customer_by_cif_number
from app.api.v1.endpoints.casa.pay_in_cash.schema import (
    PayInCashSCBToAccountRequest, PayInCashSCBByIdentity, PayInCashThirdPartyByIdentity,
    PayInCashThirdParty247ToAccount, PayInCashThirdParty247ToCard, PayInCashThirdPartyToAccount
)
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import CtrGWCasaAccount
from app.api.v1.endpoints.user.schema import AuthResponse
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.others.permission.controller import PermissionController
from app.utils.constant.approval import PAY_IN_CASH_STAGE_BEGIN
from app.utils.constant.business_type import BUSINESS_TYPE_PAY_IN_CASH
from app.utils.constant.casa import RECEIVING_METHODS, RECEIVING_METHOD_SCB_TO_ACCOUNT
from app.utils.constant.idm import IDM_MENU_CODE_OPEN_CIF, IDM_GROUP_ROLE_CODE_OPEN_CIF, IDM_PERMISSION_CODE_OPEN_CIF
from app.utils.error_messages import ERROR_RECEIVING_METHOD_NOT_EXIST, ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_NOT_NULL


class CtrPayInCash(BaseController):
    async def ctr_save_pay_in_cash_scb_to_scb(
            self,
            current_user: AuthResponse,
            request: PayInCashSCBToAccountRequest
    ):
        account_number = request.account_number

        # Kiếm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(account_number=account_number)
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
        current_user = self.current_user
        ################################################################################################################
        # VALIDATE
        ################################################################################################################
        # check quyền user
        self.call_repos(await PermissionController().ctr_approval_check_permission(
            auth_response=current_user,
            menu_code=IDM_MENU_CODE_OPEN_CIF,
            group_role_code=IDM_GROUP_ROLE_CODE_OPEN_CIF,
            permission_code=IDM_PERMISSION_CODE_OPEN_CIF,
            stage_code=PAY_IN_CASH_STAGE_BEGIN
        ))

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_PAY_IN_CASH,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        # Kiểm tra số CIF có tồn tại trong CRM không
        if cif_number:
            self.call_repos(await repos_get_customer_by_cif_number(
                cif_number=cif_number,
                session=self.oracle_session
            ))

        if is_fee and not fee_info:
            return self.response_exception(msg=ERROR_NOT_NULL, loc="fee_info")

        if receiving_method not in RECEIVING_METHODS:
            return self.response_exception(
                msg=ERROR_RECEIVING_METHOD_NOT_EXIST,
                loc=f'receiving_method: {receiving_method}'
            )

        ################################################################################################################

        pay_in_cash_info = None
        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            pay_in_cash_info = await self.ctr_save_pay_in_cash_scb_to_scb(
                current_user=current_user,
                request=request
            )

        return self.response(data=pay_in_cash_info)

