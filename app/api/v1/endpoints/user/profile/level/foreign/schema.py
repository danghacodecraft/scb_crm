from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


# Thông tin trình độ ngoại ngữ
class ForeignLanguageLevelInfoResponse(BaseSchema):
    language_type: Optional[str] = Field(..., description="Ngoại ngữ")
    level: OptionalDropdownResponse = Field(..., description="Trình độ")
    point: Optional[str] = Field(None, description="Điểm")
    certification_date: Optional[date] = Field(None, description="Ngày nhận chứng chỉ")
