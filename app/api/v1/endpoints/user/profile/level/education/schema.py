from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


# Thông tin trình độ văn hóa
class EducationLevelInfoResponse(BaseSchema):
    education_information: Optional[str] = Field(..., description="Trình độ văn hóa")
    education_level: OptionalDropdownResponse = Field(..., description="Trình độ học vấn")
    professional: Optional[str] = Field(..., description="Trình độ chuyên môn")
    major: Optional[str] = Field(..., description="Chuyên ngành")
    school: OptionalDropdownResponse = Field(..., description="Trường học")
    training_method: OptionalDropdownResponse = Field(..., description="Hình thức đào tạo")
    ranking: Optional[str] = Field(..., description="Xếp loại")
    gpa: Optional[str] = Field(..., description="Điểm tốt nghiệp")
