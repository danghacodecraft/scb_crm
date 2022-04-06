from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình công tác
class WorkProcessResponse(BaseSchema):
    from_date: Optional[date] = Field(..., description="Từ ngày")
    to_date: Optional[date] = Field(..., description="Đến ngày")
    company: Optional[str] = Field(..., description="Công ty")
    position: Optional[str] = Field(..., description="Chức vụ")
