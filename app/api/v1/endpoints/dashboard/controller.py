from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_get_customer, repos_get_transaction_list
)


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self, search_box: str):
        transaction_list = self.call_repos(await repos_get_transaction_list(
            search_box=search_box,
            session=self.oracle_session
        ))
        if search_box:
            transactions = [{
                "cif_id": transaction.id,
                "full_name_vn": transaction.full_name_vn
            } for _, transaction in transaction_list]
        else:
            transactions = [{
                "cif_id": transaction.id,
                "full_name_vn": transaction.full_name_vn
            } for transaction in transaction_list]

        transactions = transactions[:10]
        return self.response_paging(
            data=transactions,
            total_item=len(transactions)
        )

    async def ctr_get_customer_list(
            self,
            cif_number: str,
            identity_number: str,
            phone_number: str,
            full_name: str
    ):
        limit = self.pagination_params.limit

        page = 1
        if self.pagination_params.page:
            page = self.pagination_params.page

        customer = self.call_repos(await repos_get_customer(
            cif_number=cif_number,
            identity_number=identity_number,
            phone_number=phone_number,
            full_name=full_name,
            limit=limit,
            page=page,
            session=self.oracle_session))
        total = 0

        if customer:
            total = customer[0][2]

        total_page = total / limit
        if total_page % limit != 0:
            total_page += 1

        return self.response_paging(
            data=customer,
            total_item=total,
            current_page=page,
            total_page=total_page
        )
