from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.withdraw.repository import (
    repos_save_withdraw_info, repos_withdraw_info
)
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


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

    async def ctr_save_withdraw_info(self, cif_id: str, request: WithdrawRequest):
        casa_info = self.call_repos(
            await repos_save_withdraw_info(
                cif_id=cif_id,
                request=request,
                session=self.oracle_session
            )
        )

        return self.response(data=casa_info)
