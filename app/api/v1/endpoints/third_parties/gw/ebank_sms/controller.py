from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.ebank_sms.repository import (
    repos_gw_get_select_account_td_by_mobile_num,
    repos_gw_get_select_mobile_number_sms_by_account_casa
)


class CtrGWEbankSms(BaseController):
    async def ctr_gw_select_mobile_number_sms_by_account_casa(self, ebank_sms_indentify_num):
        current_user = self.current_user
        ebank_sms_info = self.call_repos(await repos_gw_get_select_mobile_number_sms_by_account_casa(
            ebank_sms_indentify_num=ebank_sms_indentify_num, current_user=current_user))

        return self.response(data=ebank_sms_info)

    async def ctr_gw_select_account_td_by_mobile_num(self, ebank_sms_indentify_num):
        current_user = self.current_user
        ebank_sms_info = self.call_repos(await repos_gw_get_select_account_td_by_mobile_num(
            ebank_sms_indentify_num=ebank_sms_indentify_num, current_user=current_user))

        return self.response(data=ebank_sms_info)
