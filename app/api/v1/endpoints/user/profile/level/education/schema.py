from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin trình độ văn hóa
class EducationLevelInfoResponse(BaseSchema):
    education_information: Optional[str] = Field(..., description="Trình độ văn hóa")
    education_level: Optional[str] = Field(..., description="Trình độ học vấn")
    professional: Optional[str] = Field(..., description="Trình độ chuyên môn")
    major: Optional[str] = Field(..., description="Chuyên ngành")
    school: Optional[str] = Field(..., description="Trường học")
    training_method: Optional[str] = Field(..., description="Hình thức đào tạo")
    ranking: Optional[str] = Field(..., description="Xếp loại")
    gpa: Optional[str] = Field(..., description="Điểm tốt nghiệp")
