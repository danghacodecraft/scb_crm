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


async def repos_gw_get_employee_list_from_org_id(
        org_id: str, current_user
):
    current_user = current_user.user_info
    is_success, employee_infos = await service_gw.get_employee_list_from_org_id(
        org_id=org_id, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_employee_list_from_org_id",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_infos)
        )

    return ReposReturn(data=employee_infos)


async def repos_gw_get_retrieve_employee_info_from_code(
        staff_code: str, current_user
):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_retrieve_employee_info_from_code(
        staff_code=staff_code,
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_employee_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_working_process_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_working_process_info_from_code(current_user=current_user)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_working_process_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_reward_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_reward_info_from_code(current_user=current_user)
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_reward_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_discipline_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_discipline_info_from_code(current_user=current_user)
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_discipline_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_topic_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_topic_info_from_code(current_user=current_user)

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_topic_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_kpis_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_kpis_info_from_code(
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_kpis_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)


async def repos_gw_get_staff_other_info_from_code(current_user):
    current_user = current_user.user_info
    is_success, employee_info = await service_gw.get_staff_other_info_from_code(current_user=current_user)
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_staff_other_info_from_code",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(employee_info)
        )

    return ReposReturn(data=employee_info)
