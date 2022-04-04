from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_foreign(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail(employee_id=employee_id)
    # data_response = {
    #     "language_type": "Anh",
    #     "level": {
    #         "id": 1,
    #         "code": "Code",
    #         "name": "B"
    #     },
    #     "gpa": None,
    #     "certification_date": None
    # }

    return ReposReturn(data=data_response)
