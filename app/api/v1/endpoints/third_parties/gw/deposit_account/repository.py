from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_deposit_account_by_cif_number(
        cif_number: str, current_user
):
    current_user = current_user.user_info
    is_success, deposit_account = await service_gw.get_deposit_account_from_cif(
        account_cif_number=cif_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_deposit_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(deposit_account)
        )

    return ReposReturn(data=deposit_account)


async def repos_gw_get_deposit_account_td(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, deposit_account_td = await service_gw.get_deposit_account_td(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_get_deposit_account_td",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(deposit_account_td)
        )

    return ReposReturn(data=deposit_account_td)
