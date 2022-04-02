from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_education(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail(employee_id=employee_id)
    # data_response = {
    #     "education_information": "12/12",
    #     "education_level": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Đại học"
    #     },
    #     "professional": "Công nghệ thông tin",
    #     "major": "Công nghệ thông tin",
    #     "school": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Trường đại học Bách Khoa Tp.HCM"
    #     },
    #     "training_method": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Chính quy"
    #     },
    #     "ranking": "Khá",
    #     "gpa": "8.0"
    # }
    return ReposReturn(data=data_response)
