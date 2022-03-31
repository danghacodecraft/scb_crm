from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_training_in_scb(
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "topic": "Kỹ năng quản lý thời gian",
            "course_code": None,
            "course_name": None,
            "from_date": "2021-06-04",
            "to_date": "2021-06-08",
            "result": "Đạt"
        }
    ]

    return ReposReturn(data=data_response)
