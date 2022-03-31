from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_it(
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "certificate": "Tin học văn phòng A",
            "level": "Kỹ thuật viên",
            "point": "7.5"
        },
        {
            "certificate": "Tin học văn phòng B",
            "level": "Kỹ thuật viên",
            "point": None
        },
        {
            "certificate": "Tin học ứng dụng",
            "level": "Kỹ thuật viên",
            "point": None
        }
    ]
    return ReposReturn(data=data_response)
