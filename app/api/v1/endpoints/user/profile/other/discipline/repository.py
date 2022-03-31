from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_discipline(
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "effective_date": None,
            "end_date": None,
            "titles": None,
            "dep_name": None,
            "disciplinary_reasons": None,
            "detailed_reason": None,
            "date_detect": None,
            "date_violation": None,
            "total_damage_value": None,
            "decision_number": None,
            "people_delete_discipline": None,
            "signer": None
        }
    ]

    return ReposReturn(data=data_response)
