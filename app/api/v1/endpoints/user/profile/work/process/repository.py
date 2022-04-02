from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_process(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail_work_process(employee_id=employee_id)
    # data_response = [
    #     {
    #         "from_date": "2019-12-4",
    #         "to_date": "2021-12-23",
    #         "company": "Ngân hàng SCB",
    #         "position": {
    #             "id": "1",
    #             "code": "Code",
    #             "name": "Chuyên viên"
    #         }
    #     }
    # ]
    return ReposReturn(data=data_response)
