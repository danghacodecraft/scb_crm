from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_work_profile(
    session: Session
) -> ReposReturn:
    data_response = {
        "working_date": "2021-06-06",
        "probationary_date": "2021-06-09",
        "official_date": "2021-06-19",
        "current": {
            "branch": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "root": {
            "branch": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "temporary": {
            "branch": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "seniority_date": "2021-09-06",
        "is_resident": True
    }

    return ReposReturn(data=data_response)
