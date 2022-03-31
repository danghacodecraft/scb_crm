from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_work_profile(
    session: Session
) -> ReposReturn:
    data_response = {
        "working_day": "06/06/2021",
        "probationary_day": "06/09/2021",
        "official_date": "15/09/2021",
        "current_unit": {
            "current_working_unit": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "company_position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "root_unit": {
            "original_unit": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "company_position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "temporary_unit": {
            "temporary_unit": {
                "id": "1",
                "code": "Code",
                "name": "Phòng quản lý khai thác, phân tích dữ liệu"
            },
            "company_position": {
                "id": "1",
                "code": "Code",
                "name": "Nhân viên"
            }
        },
        "seniority_date": "2021-09-06",
        "resident_object": True
    }

    return ReposReturn(data=data_response)
