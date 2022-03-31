from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Thông tin trình độ ngoại ngữ
class ForeignLanguageLevelInfoResponse(BaseSchema):
    foreign_language: str = Field(..., description="Ngoại ngữ")
    level: DropdownResponse = Field(..., description="Trình độ")
    point: str = Field(None, description="Điểm")
    certificate_date: date = Field(None, description="Ngày nhận chứng chỉ")
