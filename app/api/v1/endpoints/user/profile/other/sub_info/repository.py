from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_sub_info(
        employee_id: str
) -> ReposReturn:
    sub_infos = await service_dwh.sub_info(employee_id=employee_id)

    # data_response = {
    #     "recruit_info": {
    #         "code": "TD-12345",
    #         "reason": "Bổ sung nhân sự đầu năm",
    #         "introducer": "Trần Thanh Sang",
    #         "replacement_staff": "Võ Ngọc Yến",
    #         "note": None
    #     },
    #     "other_info": {
    #         "other_info": "Nhân viên lâu năm",
    #         "dateoff": "6",
    #         "annual_leave": 12
    #     }
    # }

    return ReposReturn(data=sub_infos)
