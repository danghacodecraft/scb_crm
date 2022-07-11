from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw


async def repos_training_in_scb(
        current_user: AuthResponse,
) -> ReposReturn:
    training_in_scbs = await service_gw.get_topic_info_from_code(current_user=current_user.user_info)

    return ReposReturn(data=training_in_scbs)
