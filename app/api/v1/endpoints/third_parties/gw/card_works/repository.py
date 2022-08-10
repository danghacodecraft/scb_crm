from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import service_gw


async def repos_gw_open_cards(current_user: UserInfoResponse, data):
    gw_open_cards = await service_gw.open_cards(
        current_user=current_user,
        data_input=data
    )
    return ReposReturn(data=gw_open_cards)
