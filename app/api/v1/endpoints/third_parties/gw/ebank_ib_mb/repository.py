from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_check_username_ib_mb_exist(
        transaction_name,
        transaction_value,
        current_user
):
    current_user = current_user.user_info
    is_success, check_username_ib_mb_exist = await service_gw.check_username_ib_mb_exist(
        current_user=current_user,
        transaction_name=transaction_name,
        transaction_value=transaction_value
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_check_username_ib_mb_exist",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(check_username_ib_mb_exist)
        )

    return ReposReturn(data=check_username_ib_mb_exist)
