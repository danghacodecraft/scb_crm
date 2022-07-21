from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.ebank.repository import (
    repos_gw_get_open_ib, repos_gw_get_retrieve_ebank_by_cif_number
)


class CtrGWRetrieveEbank(BaseController):
    async def ctr_gw_get_retrieve_ebank_by_cif_number(self, cif_num):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_get_retrieve_ebank_by_cif_number(
            cif_num=cif_num, current_user=current_user))
        ebank_info_list = ebank_info['retrieveEbankStatusByCif_out']['data_output']['ebank_info_list']
        response_data = []
        for ebank in ebank_info_list:
            response_data.append(dict(
                ebank_info_item=dict(
                    ebank_name=ebank['ebank_info_item']['ebank_name'],
                    ebank_status=ebank['ebank_info_item']['ebank_status']
                )
            ))

        return self.response(data=response_data)

    async def ctr_gw_open_ib(self, request):
        current_user = self.current_user
        open_ib_info = self.call_repos(await repos_gw_get_open_ib(
            request=request, current_user=current_user))

        return self.response(data=open_ib_info)
