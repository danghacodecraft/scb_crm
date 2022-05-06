from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.constant.gw import GW_TRANSACTION_NAME_ALL
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_organization_info(
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, organization_info = await service_gw.select_org_info(
        transaction_name=GW_TRANSACTION_NAME_ALL,
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_organization_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(organization_info)
        )

    return ReposReturn(data=organization_info)
