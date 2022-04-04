from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_kpi(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.kpi(employee_id=employee_id)

    # data_response = [
    #     {
    #         "assessment_period": "10/2021",
    #         "total_score": "148.64",
    #         "completion_rate": "15%",
    #         "result": "Không đạt",
    #         "note": "Đã trễ hẹn KPIs nhiều lần"
    #     }
    # ]

    return ReposReturn(data=data_response)
