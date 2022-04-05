from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_contact_info(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail(employee_id=employee_id)

    return ReposReturn(data=data_response)
