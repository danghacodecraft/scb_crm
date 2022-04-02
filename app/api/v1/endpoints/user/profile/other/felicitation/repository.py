from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_felicitation(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "effective_date": None,
            "decision_number": None,
            "titles": None,
            "rank_commend": None,
            "job_title_name": None,
            "dep_name": None,
            "reason_commend": None,
            "form_commend": None,
            "bonus_amount": None,
            "sign_day": None,
            "signer": None
        }
    ]

    return ReposReturn(data=data_response)
