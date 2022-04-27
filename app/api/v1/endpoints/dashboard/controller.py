from datetime import date

from app.api.base.controller import BaseController
from app.api.v1.endpoints.dashboard.repository import (
    repos_count_total_item, repos_get_customer, repos_get_total_item,
    repos_get_transaction_list
)
from app.utils.functions import dropdown


class CtrDashboard(BaseController):
    async def ctr_get_transaction_list(self, search_box: str, from_date: date, to_date: date):
        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        transaction_list = self.call_repos(await repos_get_transaction_list(
            search_box=search_box,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            page=current_page,
            session=self.oracle_session
        ))

        total_item = self.call_repos(await repos_count_total_item(
            search_box=search_box, from_date=from_date, to_date=to_date, session=self.oracle_session))

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        return self.response_paging(
            data=transaction_list,
            current_page=current_page,
            total_items=total_item,
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
            "cif_id": item.Customer.id,
            "cif_number": item.Customer.cif_number,
            "full_name": item.Customer.full_name_vn,
            "identity_number": item.CustomerIdentity.identity_num if item.CustomerIdentity else None,
            "phone_number": item.Customer.mobile_number,
            "street": item.CustomerAddress.address if item.CustomerAddress else None,
            "ward": dropdown(item.AddressWard) if item.AddressWard else None,
            "district": dropdown(item.AddressDistrict) if item.AddressDistrict else None,
            "province": dropdown(item.AddressProvince) if item.AddressProvince else None,
            "branch": dropdown(item.Branch) if item.Branch else None
        } for item in customers]

        return self.response_paging(
            data=response_data,
            current_page=current_page,
            total_items=total_item,
            total_page=total_page
        )
