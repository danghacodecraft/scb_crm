from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh


async def repos_profile(
        employee_id: str,
        session: Session
) -> ReposReturn:
    data_reponse = await service_dwh.detail(employee_id=employee_id)
    # data_reponse = {
    #     "full_name_vn": "NGUYỄN THỊ PHƯƠNG THẢO",
    #     "email": "nguyenvana@scb.vn",
    #     "mobile_number": "(+84)896 524 256",
    #     "code": "1234",
    #     "department": "B0-Phòng chung khối doanh nghiệp",
    #     "titles": "Phó giám đốc khối kinh doanh",
    #     "manager": "123456-Nguyễn Văn A",
    #     "telephone_number": "(+28) 123 456 789"
    # }

    return ReposReturn(data=data_reponse)
