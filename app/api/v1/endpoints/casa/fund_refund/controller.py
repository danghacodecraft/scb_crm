from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.fund_refund.repository import (
    repos_fund_info, repos_save_fund_info
)
from app.api.v1.endpoints.casa.fund_refund.schema import FundRefundRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


class CtrFund(BaseController):
    async def ctr_fund_refund_info(self, cif_id: str):  # TODO: ctr_get_fund_refund_info
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        fund_info = self.call_repos(
            await repos_fund_info(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        return self.response(data=fund_info)

    async def ctr_save_fund_refund_info(self, cif_id: str, request: FundRefundRequest):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        fund_info = self.call_repos(
            await repos_save_fund_info(
                cif_id=cif_id,
                request=request,
                session=self.oracle_session

            )
        )

        return self.response(data=fund_info)
