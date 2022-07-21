from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.branch_location.repository import (
    repos_gw_select_branch_by_branch_id, repos_gw_select_branch_by_region_id
)
from app.utils.constant.gw import (
    GW_LATITUDE_DEFAULT, GW_LATITUDE_MAX, GW_LATITUDE_MIN,
    GW_LONGITUDE_DEFAULT, GW_LONGITUDE_MAX, GW_LONGITUDE_MIN, GW_TYPE_DEFAULT
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
            branch = {
                "branch_id": region_item['branch_code'],
                "branch_name": region_item['branch_name'],
                "latitude": float(region_item['latitude']) if region_item['latitude'] != '' else 0,
                "longitude": float(region_item['longtitude']) if region_item['longtitude'] != '' else 0,
                "type": region_item['region_type']
            }
            if region_item['region_id'] not in response_datas.keys():
                response_datas.update({region_item['region_id']: (region_item['region_name'], [branch])})
            else:
                response_datas[region_item['region_id']][1].append(branch)

        res = []
        for key in response_datas.keys():
            region = {
                "region_id": key,
                "region_name": response_datas[key][0],
                "branches": response_datas[key][1]
            }
            region['branches'].insert(
                0,
                {
                    'branch_id': 'ALL',
                    'branch_name': 'Tất cả',
                    'longitude': GW_LONGITUDE_DEFAULT,
                    'latitude': GW_LATITUDE_DEFAULT,
                    'type': GW_TYPE_DEFAULT
                }
            )

            left = GW_LONGITUDE_MAX
            right = GW_LONGITUDE_MIN
            top = GW_LATITUDE_MIN
            bottom = GW_LATITUDE_MAX
            for branch in region['branches']:
                branch_id = branch['branch_code']
                longitude = branch['longitude']
                latitude = branch['latitude']
                if branch_id != 'ALL':
                    left = left if left < longitude else longitude
                    right = right if right > longitude else longitude
                    top = top if top > latitude else latitude
                    bottom = bottom if bottom < latitude else latitude

            region.update(left=left, right=right, top=top, bottom=bottom)
            res.append(region)

        if region_id == 'ALL':
            res.append({
                "region_id": "ALL",
                "region_name": "Tất cả",
                "branches": [
                    {
                        "branch_id": "ALL",
                        "branch_name": "Tất cả",
                        'longitude': GW_LONGITUDE_DEFAULT,
                        'latitude': GW_LATITUDE_DEFAULT,
                        "type": GW_TYPE_DEFAULT
                    }
                ],
                "left": GW_LONGITUDE_MIN,
                "right": GW_LONGITUDE_MAX,
                "top": GW_LATITUDE_MAX,
                "bottom": GW_LATITUDE_MIN,
            })

        res.sort(key=lambda k: k['region_id'])
        return self.response(data=res)

    async def ctr_gw_select_branch_by_branch_id(self, branch_id):
        is_success, gw_select_branch_by_branch_id = self.call_repos(await repos_gw_select_branch_by_branch_id(
            branch_id=branch_id,
            current_user=self.current_user.user_info
        ))
        if not is_success:
            return self.response_exception(msg=ERROR_CALL_SERVICE_GW, detail=str(gw_select_branch_by_branch_id))
        response_data = gw_select_branch_by_branch_id['selectBranchByBranchID_out']['data_output']
        return self.response(data={
            'region_id': response_data['region_id'],
            'region_name': response_data['region_name'],
            'branch_id': response_data['branch_code'],
            'branch_name': response_data['branch_name'],
            'latitude': response_data['latitude'],
            'longitude': response_data['longtitude'],
            'type': response_data['region_type'],
        })
