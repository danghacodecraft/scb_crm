from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_history_change_field_account(current_user):
    current_user = current_user.user_info
    is_success, history_change_field = await service_gw.get_history_change_field(
        current_user=current_user
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_history_change_field_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(history_change_field)
        )

    return ReposReturn(data=history_change_field)
