from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import repos_withdraw_info
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.api.v1.others.booking.controller import CtrBooking
from app.utils.constant.business_type import (
    BUSINESS_TYPE_OPEN_CASA, BUSINESS_TYPE_WITHDRAW
)


class CtrWithdraw(BaseController):
    async def ctr_withdraw_info(self, cif_id: str):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        casa_info = self.call_repos(
            await repos_withdraw_info(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        return self.response(data=casa_info)

    async def ctr_save_withdraw_info(self, booking_id: str, request: WithdrawRequest):
        # Check exist Booking
        await CtrBooking().ctr_get_booking_and_validate(
            business_type_code=BUSINESS_TYPE_OPEN_CASA,
            booking_id=booking_id,
            check_correct_booking_flag=False,
            loc=f"header -> booking-id, booking_id: {booking_id}, business_type_code: {BUSINESS_TYPE_WITHDRAW}"
        )

        return self.response(data="casa_info")
