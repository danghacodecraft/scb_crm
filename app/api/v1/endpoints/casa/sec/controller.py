from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.sec.schema import SecRequest
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import BUSINESS_TYPE_SEC
from app.utils.error_messages import ERROR_CASA_ACCOUNT_NOT_EXIST


class CtrSecInfo(BaseController):
    async def ctr_sec_info(
            self,
            booking_id: str,
            account_num: str,
            request: SecRequest
    ):
        current_user = self.current_user
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=booking_id,
            business_type_code=BUSINESS_TYPE_SEC,
            check_correct_booking_flag=False,
            loc=f'booking_id: {booking_id}'
        )

        # Kiểm tra số tài khoản có tồn tại hay không
        casa_account = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
            account_number=account_num
        )
        if not casa_account['data']['is_existed']:
            return self.response_exception(
                msg=ERROR_CASA_ACCOUNT_NOT_EXIST,
                loc=f"account_number: {account_num}"
            )

        return self.response(data='a')
