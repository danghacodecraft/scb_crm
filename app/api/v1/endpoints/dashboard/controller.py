from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_count_total_item, repos_get_customer, repos_get_total_item,
    repos_get_transaction_list
)
from app.utils.functions import dropdown


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self, search_box: str):
        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        transaction_list = self.call_repos(await repos_get_transaction_list(
            search_box=search_box,
            limit=limit,
            page=current_page,
            session=self.oracle_session
        ))

        if search_box:
            transactions = [{
                "cif_id": transaction.id,
                "full_name_vn": transaction.full_name_vn
            } for _, transaction in transaction_list]
        else:
            transactions = [{
                "cif_id": transaction[0].id,
                "full_name_vn": transaction[0].full_name_vn
            } for transaction in transaction_list]

        total_item = self.call_repos(await repos_count_total_item(search_box=search_box, session=self.oracle_session))

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        return self.response_paging(
            data=transactions,
            current_page=current_page,
            total_item=total_item,
            total_page=total_page
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

        total_item = self.call_repos(
            await repos_get_total_item(
                cif_number=cif_number,
                identity_number=identity_number,
                phone_number=phone_number,
                full_name=full_name,
                session=self.oracle_session
            )
        )

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        response_data = [{
            "cif_number": item.Customer.cif_number,
            "full_name": item.Customer.full_name_vn,
            "identity_number": item.CustomerIdentity.identity_num,
            "phone_number": item.Customer.mobile_number,
            "street": item.CustomerAddress.address,
            "ward": dropdown(item.AddressWard),
            "district": dropdown(item.AddressDistrict),
            "province": dropdown(item.AddressProvince),
            "branch": dropdown(item.Branch)
        } for item in customers]

        return self.response_paging(
            data=response_data,
            current_page=current_page,
            total_item=total_item,
            total_page=total_page
        )
