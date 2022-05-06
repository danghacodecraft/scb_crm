from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.constant.gw import (
    GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO,
    GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_CHILD,
    GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_PARENT,
    GW_ORGANIZATION_FROM_CHILD_ID, GW_ORGANIZATION_ID,
    GW_ORGANIZATION_INFO_FROM_CHILD_NAME,
    GW_ORGANIZATION_INFO_FROM_PARENT_NAME, GW_ORGANIZATION_INFO_NAME,
    GW_TRANSACTION_NAME_ALL, GW_TRANSACTION_NAME_CHILD,
    GW_TRANSACTION_NAME_PARENT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_organization_info(
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, organization_info = await service_gw.select_org_info(
        transaction_name=GW_TRANSACTION_NAME_ALL,
        current_user=current_user,
        endpoint=GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO,
        function_name=GW_ORGANIZATION_INFO_NAME,
        id=GW_ORGANIZATION_ID
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_organization_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(organization_info)
        )

    return ReposReturn(data=organization_info)


async def repos_gw_get_organization_info_from_parent(
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, organization_info_from_parent = await service_gw.select_org_info(
        transaction_name=GW_TRANSACTION_NAME_PARENT,
        current_user=current_user,
        endpoint=GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_PARENT,
        function_name=GW_ORGANIZATION_INFO_FROM_PARENT_NAME,
        id=GW_ORGANIZATION_ID
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_organization_info_from_parent",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(organization_info_from_parent)
        )

    return ReposReturn(data=organization_info_from_parent)


async def repos_gw_get_organization_info_from_child(
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, organization_info_from_child = await service_gw.select_org_info(
        transaction_name=GW_TRANSACTION_NAME_CHILD,
        current_user=current_user,
        endpoint=GW_ENDPOINT_URL_RETRIEVE_ORGANIZATION_INFO_FROM_CHILD,
        function_name=GW_ORGANIZATION_INFO_FROM_CHILD_NAME,
        id=GW_ORGANIZATION_FROM_CHILD_ID
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_organization_info_from_child",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(organization_info_from_child)
        )

    return ReposReturn(data=organization_info_from_child)
