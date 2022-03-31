from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_education(
        session: Session
) -> ReposReturn:
    data_response = {
        "level_information": "12/12",
        "education_level": {
            "id": "1",
            "code": "Code",
            "name": "Đại học"
        },
        "professional_qualification": "Công nghệ thông tin",
        "specialized": "Công nghệ thông tin",
        "school": {
            "id": "1",
            "code": "Code",
            "name": "Trường đại học Bách Khoa Tp.HCM"
        },
        "forms_training": {
            "id": "1",
            "code": "Code",
            "name": "Chính quy"
        },
        "degree": "Khá",
        "point_graduate": "8.0"
    }
    return ReposReturn(data=data_response)
