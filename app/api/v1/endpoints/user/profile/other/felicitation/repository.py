from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_felicitation(
        employee_id: str,
) -> ReposReturn:
    felicitations = await service_dwh.felicitation(employee_id=employee_id)

    return ReposReturn(data=felicitations)
