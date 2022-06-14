from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_select_category(
        transaction_name: str,
        transaction_value: str,
        current_user: AuthResponse
):
    is_success, select_category = await service_gw.get_select_category(
        transaction_name=transaction_name,
        transaction_value=transaction_value,
        current_user=current_user.user_info
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_select_category",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(select_category)
        )
    return ReposReturn(data=select_category)
