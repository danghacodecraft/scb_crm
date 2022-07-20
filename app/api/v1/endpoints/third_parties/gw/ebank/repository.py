from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_retrieve_ebank_by_cif_number(
        cif_num: str, current_user
):
    current_user = current_user.user_info
    is_success, retrieve_ebank = await service_gw.get_retrieve_ebank_td(
        cif_num=cif_num, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_ebank_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(retrieve_ebank)
        )

    return ReposReturn(data=retrieve_ebank)
