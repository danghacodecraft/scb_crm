from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.ebank.repository import (
    repos_gw_get_open_ib, repos_gw_get_retrieve_ebank_by_cif_number,
    repos_gw_get_retrieve_internet_banking_by_cif_number
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

    async def ctr_gw_get_retrieve_internet_banking_by_cif_number(self, cif_num):
        current_user = self.current_user
        internet_banking_info = self.call_repos(await repos_gw_get_retrieve_internet_banking_by_cif_number(
            cif_num=cif_num, current_user=current_user))
        internet_banking_info_list = internet_banking_info['retrieveIBInfoByCif_out']['data_output']['ebank_ibmb_info']

        response_data = []
        for internet_banking in internet_banking_info_list:

            ebank_ibmb_authentication_info_list = []
            for ebank_ibmb_authentication_info in internet_banking['ebank_ibmb_authentication_info_list']:
                ebank_ibmb_authentication_info_list.append(
                    dict(
                        ebank_ibmb_authentication_info_item=dict(
                            authentication_code=ebank_ibmb_authentication_info['ebank_ibmb_authentication_info_item']['authentication_code'],
                            authentication_name=ebank_ibmb_authentication_info['ebank_ibmb_authentication_info_item']['authentication_name']
                        )
                    )
                )

            response_data.append(dict(
                ebank_ibmb_username=internet_banking['ebank_ibmb_username'],
                ebank_ibmb_email=internet_banking['ebank_ibmb_email'],
                ebank_ibmb_active_date=internet_banking['ebank_ibmb_active_date'],
                ebank_ibmb_reg_date=internet_banking['ebank_ibmb_reg_date'],
                ebank_ibmb_status=internet_banking['ebank_ibmb_status'],
                ebank_ibmb_mobilephone=internet_banking['ebank_ibmb_mobilephone'],
                ebank_ibmb_notify_mode=internet_banking['ebank_ibmb_notify_mode'],
                ebank_ibmb_latest_login=internet_banking['ebank_ibmb_latest_login'],
                ebank_ibmb_staff_info=dict(
                    staff_code=internet_banking['ebank_ibmb_username']
                ),
                ebank_ibmb_service_pack_info=dict(
                    service_package_code=internet_banking['ebank_ibmb_service_pack_info']['service_package_code'],
                    service_package_name=internet_banking['ebank_ibmb_service_pack_info']['service_package_name']
                ),
                ebank_ibmb_receive_password_info=dict(
                    receive_password_code=internet_banking['ebank_ibmb_receive_password_info']['receive_password_code'],
                    receive_password_name=internet_banking['ebank_ibmb_receive_password_info']['receive_password_name']
                ),
                ebank_ibmb_authentication_info_list=ebank_ibmb_authentication_info_list,
                ebank_ibmb_branch_info=dict(
                    branch_code=internet_banking['ebank_ibmb_branch_info']['branch_code']
                ),
            ))

        return self.response(data=response_data)

    async def ctr_gw_open_ib(self, request):
        current_user = self.current_user
        open_ib_info = self.call_repos(await repos_gw_get_open_ib(
            request=request, current_user=current_user))

        return self.response(data=open_ib_info)
