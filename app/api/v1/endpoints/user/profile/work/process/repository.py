from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw


async def repos_process_info(
        current_user: AuthResponse
) -> ReposReturn:

    is_success, data_response = await service_gw.get_working_process_info_from_code(
        current_user=current_user.user_info)

    if not is_success:
        return ReposReturn(is_error=True, msg=str(data_response), loc="employee_working_process'")

    return ReposReturn(data=data_response)
