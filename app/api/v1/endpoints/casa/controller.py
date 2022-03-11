from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.repository import (
    repos_casa_info, repos_save_casa_info
)
from app.api.v1.endpoints.casa.schema import WithdrawResponse
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


class CtrCasa(BaseController):
    async def ctr_casa_info(self, cif_id: str):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        casa_info = self.call_repos(
            await repos_casa_info(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        return self.response(data=casa_info)

    async def ctr_save_casa_info(self, cif_id: str, request: WithdrawResponse):
        casa_info = self.call_repos(
            await repos_save_casa_info(
                cif_id=cif_id,
                request=request,
                session=self.oracle_session
            )
        )

        return self.response(data=casa_info)
