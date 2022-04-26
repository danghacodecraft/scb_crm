from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình đào tạo trong ngân hàng
class TrainingInSCBResponse(BaseSchema):
    topic: Optional[str] = Field(..., description="Chủ đề")
    code: Optional[str] = Field(None, description="Mã khóa học")
    name: Optional[str] = Field(None, description="Tên khóa học")
    from_date: Optional[date] = Field(..., description="Từ ngày")
    to_date: Optional[date] = Field(..., description="Đến ngày")
    result: Optional[str] = Field(..., description="Kết quả")
