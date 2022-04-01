from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_process(
        session: Session
) -> ReposReturn:
    data_response = [
        {
            "from_date": "2019-12-4",
            "to_date": "2021-12-23",
            "company": "Ngân hàng SCB",
            "position": {
                "id": "1",
                "code": "Code",
                "name": "Chuyên viên"
            }
        }
    ]
    return ReposReturn(data=data_response)
