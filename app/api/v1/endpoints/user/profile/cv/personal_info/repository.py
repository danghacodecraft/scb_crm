from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_personal_info(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.detail(employee_id=employee_id)
    # data_response = {
    #     "date_of_birth": "1990-10-01",
    #     "place_of_birth": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Tp.HCM"
    #     },
    #     "gender": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Nữ"
    #     },
    #     "ethnic": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Kinh"
    #     },
    #     "religion": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Thiên chúa giáo"
    #     },
    #     "nationality": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Việt Nam"
    #     },
    #     "marital_status": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Đã kết hôn"
    #     },
    #     "identity_number": "0123456789",
    #     "issued_date": "2003-10-01",
    #     "expired_date": None,
    #     "place_of_issue": {
    #         "id": "1",
    #         "code": "Code",
    #         "name": "Tp.HCM"
    #     }
    # }

    return ReposReturn(data=data_response)
