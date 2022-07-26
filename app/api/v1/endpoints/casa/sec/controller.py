from app.api.v1.endpoints.casa.controller import CtrCasa
from app.api.v1.endpoints.casa.sec.schema import SaveSecRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_OPEN_SEC
from app.utils.constant.casa import CASA_FEE_METHOD_CASA, CASA_FEE_METHODS
from app.utils.error_messages import (
    CASA_FEE_METHOD_NOT_EXIST, ERROR_CASA_ACCOUNT_NOT_EXIST
)


class CtrSecInfo(CtrCasa):
    async def ctr_save_open_sec_info(
            self,
            booking_id: str,
            request: SaveSecRequest
    ):
        current_user = self.current_user
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_OPEN_SEC,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        # Thông tin Tài khoản
        for account_info in request.account_infos:
            # Kiểm tra số tài khoản có tồn tại hay không
            account_number = account_info.account_number
            casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
                account_number=account_number
            )
            if not casa_account['data']['is_existed']:
                return self.response_exception(
                    msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                    loc=f"transaction_info -> account_info -> account_number: {account_number}"
                )

        # Thông tin phí
        fee_info = request.transaction_info.fee_info
        if fee_info:
            method = fee_info.method
            if method not in CASA_FEE_METHODS:
                return self.response_exception(msg=CASA_FEE_METHOD_NOT_EXIST)

            if method == CASA_FEE_METHOD_CASA:
                # Kiểm tra số tài khoản có tồn tại hay không
                account_number = fee_info.account_number
                casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
                    account_number=account_number
                )
                if not casa_account['data']['is_existed']:
                    return self.response_exception(
                        msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                        loc=f"transaction_info -> fee_info -> account_number: {account_number}"
                    )

                # Bảng kê
                await self.validate_statement(statement=request.transaction_info.statement)

                # Thông tin khách hàng giao dịch
                await self.validate_sender(sender=request.transaction_info.sender)

        return self.response(data='a')
