from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình công tác
class WorkProcessResponse(BaseSchema):
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")
    company: str = Field(..., description="Công ty")
    position: str = Field(..., description="Chức vụ")
