from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_decisive_contract(
        session: Session
) -> ReposReturn:
    data_response = {
        "type": {
            "id": "1",
            "code": "Code",
            "name": "Không xác định thời hạn"
        },
        "number": "158/HĐLĐ-SCB-2014",
        "start_day": "2021-09-06",
        "end_date": None,
        "contract_addendum": {
            "number": None,
            "start_day": None,
            "end_date": None,
        },
        "date_resign": None
    }

    return ReposReturn(data=data_response)
