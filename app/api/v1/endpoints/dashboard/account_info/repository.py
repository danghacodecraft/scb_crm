from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def get_casa_account_from_cif(
        cif_number: str,
) -> ReposReturn:
    is_success, casa_account = await service_gw.get_casa_account_from_cif(
        casa_cif_number=cif_number
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(casa_account)
        )

    return ReposReturn(data=casa_account)


async def get_deposit_account_by_cif_number(
        cif_number: str,
        current_user: str
):
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
