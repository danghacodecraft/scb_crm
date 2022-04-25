from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_casa_account_by_cif_number(
        cif_number: str, current_user: AuthResponse
):
    is_success, casa_accounts = await service_gw.get_casa_account_from_cif(
        casa_cif_number=cif_number, current_user=current_user.user_info
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(casa_accounts)
        )

    for casa_account in casa_accounts:
        pass

    return ReposReturn(data=casa_accounts)


async def repos_gw_get_casa_account_info(
        account_number: str,
        current_user: str
):
    is_success, gw_casa_account_info = await service_gw.get_casa_account(
        current_user=current_user,
        account_number=account_number
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_casa_account_info)
        )

    return ReposReturn(data=gw_casa_account_info)
