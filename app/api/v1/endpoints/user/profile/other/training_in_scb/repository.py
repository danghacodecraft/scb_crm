from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_training_in_scb(
        employee_id: str,
) -> ReposReturn:

    training_in_scbs = await service_dwh.training_in_scb(employee_id=employee_id)

    # data_response = [
    #     {
    #         "topic": "Kỹ năng quản lý thời gian",
    #         "course_code": None,
    #         "course_name": None,
    #         "from_date": "2021-06-04",
    #         "to_date": "2021-06-08",
    #         "result": "Đạt"
    #     }
    # ]

    return ReposReturn(data=training_in_scbs)
