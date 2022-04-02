from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_discipline(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.other(employee_id=employee_id)
    # data_response = [
    #     {
    #         "effective_date": None,
    #         "end_date": None,
    #         "titles": None,
    #         "dep_name": None,
    #         "disciplinary_reasons": None,
    #         "detailed_reason": None,
    #         "date_detect": None,
    #         "date_violation": None,
    #         "total_damage_value": None,
    #         "decision_number": None,
    #         "people_delete_discipline": None,
    #         "signer": None
    #     }
    # ]

    return ReposReturn(data=data_response)
