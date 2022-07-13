from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import service_gw


async def repos_gw_select_branch_by_region_id(current_user: UserInfoResponse, region_id: str):
    data_input = {
        "region_id": region_id
    }
    gw_select_branch_by_region_id = await service_gw.select_branch_by_region_id(
        current_user=current_user,
        data_input=data_input
    )
    return ReposReturn(data=gw_select_branch_by_region_id)
