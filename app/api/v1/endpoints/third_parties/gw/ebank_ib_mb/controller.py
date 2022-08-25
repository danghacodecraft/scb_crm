import json

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.repository import (
    repos_gw_get_check_username_ib_mb_exist, repos_gw_open_mb,
    repos_gw_retrieve_ib_info_by_cif, repos_gw_retrieve_mb_info_by_cif,
    repos_gw_select_service_pack_ib, repos_gw_summary_bp_trans_by_invoice,
    repos_gw_summary_bp_trans_by_service
)


class CtrGWEbankIbMb(BaseController):
    async def ctr_gw_check_username_ib_mb_exist(self, transaction_name, transaction_value):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_get_check_username_ib_mb_exist(
            current_user=current_user,
            transaction_name=transaction_name,
            transaction_value=transaction_value,
            session=self.oracle_session))

        return self.response(data=ebank_info)

    async def ctr_gw_retrieve_ib_info_by_cif(self, cif_num):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_retrieve_ib_info_by_cif(
            current_user=current_user,
            cif_num=cif_num))

        return self.response(data=ebank_info)

    async def ctr_gw_retrieve_mb_info_by_cif(self, cif_num):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_retrieve_mb_info_by_cif(
            current_user=current_user,
            cif_num=cif_num))

        return self.response(data=ebank_info)

    async def ctr_gw_summary_bp_trans_by_service(self, cif_num, transaction_val_date, transaction_val_date_to_date):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_summary_bp_trans_by_service(
            current_user=current_user,
            cif_num=cif_num,
            transaction_val_date=transaction_val_date,
            transaction_val_date_to_date=transaction_val_date_to_date
        ))

        return self.response(data=ebank_info)

    async def ctr_gw_summary_bp_trans_by_invoice(self, cif_num, transaction_val_date, transaction_val_date_to_date):
        current_user = self.current_user
        ebank_info = self.call_repos(await repos_gw_summary_bp_trans_by_invoice(
            current_user=current_user,
            cif_num=cif_num,
            transaction_val_date=transaction_val_date,
            transaction_val_date_to_date=transaction_val_date_to_date
        ))

        return self.response(data=ebank_info)

    async def ctr_gw_open_mb(self, data_input):
        current_user = self.current_user
        try:
            data_input = json.loads(data_input)
        except Exception as e:
            return self.response_exception(msg=f'GW OpenMb: {e}')

        ebank_info = self.call_repos(await repos_gw_open_mb(
            current_user=current_user,
            data_input=data_input
        ))

        return self.response(data=ebank_info)

    async def ctr_gw_select_service_pack_ib(self):
        current_user = self.current_user

        ebank_info = self.call_repos(await repos_gw_select_service_pack_ib(
            current_user=current_user
        ))

        return self.response(data=ebank_info)
