from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn


async def repos_education(
        session: Session
) -> ReposReturn:
    data_response = {
        "education_information": "12/12",
        "education_level": {
            "id": "1",
            "code": "Code",
            "name": "Đại học"
        },
        "professional": "Công nghệ thông tin",
        "major": "Công nghệ thông tin",
        "school": {
            "id": "1",
            "code": "Code",
            "name": "Trường đại học Bách Khoa Tp.HCM"
        },
        "training_method": {
            "id": "1",
            "code": "Code",
            "name": "Chính quy"
        },
        "ranking": "Khá",
        "gpa": "8.0"
    }
    return ReposReturn(data=data_response)
