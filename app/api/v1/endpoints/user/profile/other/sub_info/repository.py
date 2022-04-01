from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_sub_info(
        session: Session
) -> ReposReturn:
    data_response = {
        "recruit_info": {
            "code": "TD-12345",
            "reason": "Bổ sung nhân sự đầu năm",
            "introducer": "Trần Thanh Sang",
            "replacement_staff": "Võ Ngọc Yến",
            "note": None
        },
        "other_info": {
            "other_info": "Nhân viên lâu năm",
            "dateoff": "6",
            "annual_leave": 12
        }
    }

    return ReposReturn(data=data_response)
