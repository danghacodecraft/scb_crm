from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.repository import (
    repos_gw_get_check_username_ib_mb_exist, repos_gw_retrieve_ib_info_by_cif
)


class CtrGWEbankIbMb(BaseController):
    async def ctr_gw_check_username_ib_mb_exist(self, transaction_name, transaction_value):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_get_check_username_ib_mb_exist(
            current_user=current_user,
            transaction_name=transaction_name,
            transaction_value=transaction_value))

        return self.response(data=ebank_info)

    async def ctr_gw_retrieve_ib_info_by_cif(self, cif_num):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_retrieve_ib_info_by_cif(
            current_user=current_user,
            cif_num=cif_num))

        return self.response(data=ebank_info)
