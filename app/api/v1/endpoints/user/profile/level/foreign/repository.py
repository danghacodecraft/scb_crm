from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_foreign(
        session: Session
) -> ReposReturn:
    data_response = {
        "language_type": "Anh",
        "level": {
            "id": 1,
            "code": "Code",
            "name": "B"
        },
        "gpa": None,
        "certification_date": None
    }

    return ReposReturn(data=data_response)
