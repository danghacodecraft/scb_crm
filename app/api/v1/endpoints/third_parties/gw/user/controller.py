from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.user.repository import (
    repos_gw_detail_user
)


class CtrGWUser(BaseController):

    async def ctr_gw_detail_user(self, user_id: str):
        current_user = self.current_user
        data_input = {
            "staff_info": {
                "staff_code": user_id
            }
        }
        gw_detail_user_responses = self.call_repos(await repos_gw_detail_user(
            current_user=current_user,
            data_input=data_input
        ))
        data_output = gw_detail_user_responses.get('selectUserInfoByUserID_out')
        detail_user_info = [{
            "user_code": item.get('user_code'),
            "staff_info": item.get('staff_info'),
            "branch_info": item.get('branch_info'),
            "current_date": item.get('current_date')
        }for item in data_output.get('data_output', [])]

        return self.response(data=detail_user_info)
