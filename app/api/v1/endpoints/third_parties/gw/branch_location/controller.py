from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.branch_location.repository import (
    repos_gw_select_branch_by_branch_id, repos_gw_select_branch_by_region_id
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


class CtrGWBranchLocation(BaseController):
    async def ctr_gw_select_branch_by_region_id(self, region_id):
        is_success, gw_select_branch_by_region_id = self.call_repos(await repos_gw_select_branch_by_region_id(
            region_id=region_id,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_branch_by_region_id))
        return self.response(data=[item['region_info_item'] for item in gw_select_branch_by_region_id['selectBranchByRegionID_out']['data_output']['region_info_list']])

    async def ctr_gw_select_branch_by_branch_id(self, branch_id):
        is_success, gw_select_branch_by_branch_id = self.call_repos(await repos_gw_select_branch_by_branch_id(
            branch_id=branch_id,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_branch_by_branch_id))
        return self.response(data=gw_select_branch_by_branch_id['selectBranchByBranchID_out']['data_output'])
