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
        region_info_list = gw_select_branch_by_region_id['selectBranchByRegionID_out']['data_output'][
            'region_info_list']

        region_list_item = [item['region_info_item'] for item in region_info_list]

        response_datas = {}
        for region_item in region_list_item:
            if region_item['region_id'] not in response_datas.keys():
                response_datas.update({region_item['region_id']: (region_item['region_name'], [{
                    "area_id": region_item['area_id'],
                    "area_name": region_item['area_name'],
                    "branch_console": region_item['branch_console'],
                    "branch_console_name": region_item['branch_console_name'],
                    "branch_id": region_item['branch_id'],
                    "branch_name": region_item['branch_name'],
                    "latitude": region_item['latitude'],
                    "longtitude": region_item['longtitude'],
                    "region_type": region_item['region_type']
                }])})
            else:
                response_datas[region_item['region_id']][1].append({
                    "area_id": region_item['area_id'],
                    "area_name": region_item['area_name'],
                    "branch_console": region_item['branch_console'],
                    "branch_console_name": region_item['branch_console_name'],
                    "branch_id": region_item['branch_id'],
                    "branch_name": region_item['branch_name'],
                    "latitude": region_item['latitude'],
                    "longtitude": region_item['longtitude'],
                    "region_type": region_item['region_type']
                })

        return self.response(data=[{
            "region_id": key,
            "region_name": response_datas[key][0],
            "branches": response_datas[key][1]
        } for key in response_datas.keys()]
        )

    async def ctr_gw_select_branch_by_branch_id(self, branch_id):
        is_success, gw_select_branch_by_branch_id = self.call_repos(await repos_gw_select_branch_by_branch_id(
            branch_id=branch_id,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_branch_by_branch_id))
        return self.response(data=gw_select_branch_by_branch_id['selectBranchByBranchID_out']['data_output'])
