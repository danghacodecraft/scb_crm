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

    async def ctr_get_customer_list(self, cif_number: str, identity_number: str, phone_number: str, full_name: str):

        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        customers = self.call_repos(await repos_get_customer(
            cif_number=cif_number,
            identity_number=identity_number,
            phone_number=phone_number,
            full_name=full_name,
            limit=limit,
            page=current_page,
            session=self.oracle_session))

        total_item = 0
        if customers:
            total_item = customers[0][2]

        total_page = total_item / limit
        if total_page % limit != 0:
            total_page += 1

        response_data = [{
            "cif_number": item.Customer.cif_number,
            "full_name": item.Customer.full_name,
            "identity_number": item.CustomerIdentity.identity_num,
            "phone_number": item.Customer.mobile_number,
            "street": item.CustomerAddress.address,
            "ward": item.AddressWard.name,
            "district": item.AddressDistrict.name,
            "province": item.AddressProvince.name,
            "branch_code": item.Branch.code,
            "branch_name": item.Branch.name
        } for item in customers]

        return self.response_paging(
            data=response_data,
            current_page=current_page,
            total_item=total_item,
            total_page=total_page
        )
