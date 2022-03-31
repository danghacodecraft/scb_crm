from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_kpi(
        session: Session
) -> ReposReturn:
    data_reponse = [
        {
            "assessment_period": "10/2021",
            "total_score_kpis": "148.64",
            "completion_rate": "15%",
            "result": "Không đạt",
            "note": "Đã trễ hẹn KPIs nhiều lần"
        }
    ]

    return ReposReturn(data=data_reponse)
