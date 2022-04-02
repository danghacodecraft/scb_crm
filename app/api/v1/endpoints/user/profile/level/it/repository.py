from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_it(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail(employee_id=employee_id)
    # data_response = [
    #     {
    #         "certification": "Tin học văn phòng A",
    #         "level": "Kỹ thuật viên",
    #         "gpa": "7.5"
    #     }
    # ]
    return ReposReturn(data=data_response)
