from app.api.base.controller import BaseController
from app.api.v1.endpoints.casa.fund_refund.repository import (
    repos_fund_info, repos_save_fund_info
)
from app.api.v1.endpoints.casa.fund_refund.schema import FundRefundRequest
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


class CtrFund(BaseController):
    async def ctr_get_fund_refund_info(self, cif_id: str):  # TODO: ctr_get_fund_refund_info
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

        r_transaction_code, r_transaction_type, r_invoice_list = self.call_repos(
            await repos_save_fund_info(
                cif_id=cif_id,
                request=request,
                session=self.oracle_session
            )
        )

        sealed_bags = [{
            "id": item.id,
            "amount": item.amount,
            "status": item.status,
            "selected_flag": item.selected_flag,
        } for item in r_transaction_type.sealed_bags]
        transaction_type = {
            "is_fund_flag": r_transaction_type.is_fund_flag,
            "is_main_fund_flag": r_transaction_type.is_main_fund_flag,
            "till_or_vault": r_transaction_type.till_or_vault,
            "full_name_vn": r_transaction_type.full_name_vn,
            "position": r_transaction_type.position,
            "currency": r_transaction_type.currency,
            "amount": r_transaction_type.amount,
            "content": r_transaction_type.content,
            "sealed_bags": sealed_bags
        }
        invoice_list = [{
            "denomination": item.denomination,
            "quantity": item.quantity,
            "total": item.denomination * item.quantity,
        } for item in r_invoice_list]

        invoice_details = {
            "invoice_list": invoice_list,
        }

        fund_info = {
            "transaction_code": r_transaction_code,
            "transaction_type": transaction_type,
            "invoice_details": invoice_details,
        }

        return self.response(data=fund_info)
