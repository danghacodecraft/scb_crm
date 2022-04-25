from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_gw_get_customer_info_detail, repos_gw_get_customer_info_list
)


class CtrGWCustomer(BaseController):
    async def ctr_gw_get_customer_info_list(
            self,
            cif_number: str
    ):
        current_user = self.current_user
        customer_info_list = self.call_repos(await repos_gw_get_customer_info_list(
            cif_number=cif_number, current_user=current_user))
        response_data = {}
        customer_list = customer_info_list["selectCustomerRefDataMgmtCIFNum_out"]["data_output"]["customer_list"]

        customer_list_info = []

        for customer in customer_list:
            customer_list_info.append(customer["customer_info_item"])

        response_data.update({
            "customer_info_list": customer_list_info,
            "total_items": len(customer_list_info)
        })

        return self.response(data=response_data)

    async def ctr_gw_get_customer_info_detail(self, cif_number: str):
        current_user = self.current_user
        customer_info_detail = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number, current_user=current_user))

        customer_info = customer_info_detail['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info']

        return self.response(data=customer_info)

    async def ctr_gw_check_exist_customer_detail_info(
        self,
        cif_number: str
    ):
        gw_check_exist_customer_detail_info = self.call_repos(await repos_gw_get_customer_info_detail(
            cif_number=cif_number,
            current_user=self.current_user
        ))
        customer_info = gw_check_exist_customer_detail_info['retrieveCustomerRefDataMgmt_out']['data_output']['customer_info'][
            'id_info']

        return self.response(data=dict(
            is_existed=True if customer_info['id_num'] else False
        ))
