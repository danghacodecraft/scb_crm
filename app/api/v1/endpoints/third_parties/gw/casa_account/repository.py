from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_casa_account_by_cif_number(
    cif_number: str, current_user: AuthResponse
):
    is_success, casa_account = await service_gw.get_casa_account_from_cif(
        casa_cif_number=cif_number, current_user=current_user.user_info
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(casa_account)
        )

    return ReposReturn(data=casa_account)
