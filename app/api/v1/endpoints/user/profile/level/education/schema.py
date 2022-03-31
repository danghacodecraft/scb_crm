from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Thông tin trình độ văn hóa
class CulturalLevelInfoResponse(BaseSchema):
    level_information: str = Field(..., description="Trình độ văn hóa")
    education_level: DropdownResponse = Field(..., description="Trình độ học vấn")
    professional_qualification: str = Field(..., description="Trình độ chuyên môn")
    specialized: str = Field(..., description="Chuyên ngành")
    school: DropdownResponse = Field(..., description="Đại học")
    forms_training: DropdownResponse = Field(..., description="Hình thức đào tạo")
    degree: str = Field(..., description="Xếp loại")
    point_graduate: str = Field(..., description="Điểm tốt nghiệp")
