from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_employee_info_from_code(
        employee_code: str, current_user
):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_employee_info_from_code(
        employee_code=employee_code, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_employee_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_employee_info_from_user_name(
        employee_name: str, current_user
):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_employee_info_from_user_name(
        employee_name=employee_name, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_employee_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)
