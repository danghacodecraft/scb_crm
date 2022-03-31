from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_foreign(
        session: Session
) -> ReposReturn:
    data_response = {
        "foreign_language": "Anh",
        "level": {
            "id": 1,
            "code": "Code",
            "name": "B"
        },
        "point": None,
        "certificate_date": None
    }

    return ReposReturn(data=data_response)
