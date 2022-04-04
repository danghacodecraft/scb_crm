from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_discipline(
        employee_id: str,
) -> ReposReturn:
    data_response = await service_dwh.discipline(employee_id=employee_id)

    return ReposReturn(data=data_response)
