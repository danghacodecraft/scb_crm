from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_it(
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "certification": "Tin học văn phòng A",
            "level": "Kỹ thuật viên",
            "gpa": "7.5"
        }
    ]
    return ReposReturn(data=data_response)
