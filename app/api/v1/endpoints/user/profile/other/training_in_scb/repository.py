from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_training_in_scb(
        employee_id: str,
) -> ReposReturn:
    training_in_scbs = await service_dwh.training_in_scb(employee_id=employee_id)

    return ReposReturn(data=training_in_scbs)
