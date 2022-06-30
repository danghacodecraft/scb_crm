from app.api.base.controller import BaseController


class CtrDeposit(BaseController):
    async def ctr_save_deposit_open_td_account(
            self,
            booking_id,
            deposit_account_request
    ):
        response_data = {}

        return self.response(data=response_data)
