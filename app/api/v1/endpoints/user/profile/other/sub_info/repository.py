from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_sub_info(
        employee_id: str
) -> ReposReturn:
    sub_infos = await service_dwh.sub_info(employee_id=employee_id)

    return ReposReturn(data=sub_infos)
