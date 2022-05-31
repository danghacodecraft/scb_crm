from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.history.repository import (
    repos_gw_get_history_change_field_account
)


class CtrGWHistory(BaseController):
    async def ctr_gw_get_history_change_field_account(self):
        current_user = self.current_user
        gw_history_info = self.call_repos(
            await repos_gw_get_history_change_field_account(
                current_user=current_user
            ))

        history_infos = gw_history_info["historyChangeFieldAccount_out"]["data_output"]

        return self.response(data=[dict(
            maker=history_info['maker'],
            maker_time_stamp=history_info['maker_time_stamp'],
            checker=history_info['checker'],
            checker_time_stamp=history_info['checker_time_stamp'],
            field_name=history_info['field_name'],
            old_value=history_info['old_value'],
            new_value=history_info['new_value']
        ) for history_info in history_infos])
