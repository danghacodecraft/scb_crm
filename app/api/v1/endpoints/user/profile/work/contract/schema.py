from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Số phụ lục hợp đồng
class ContractAddendumResponse(BaseSchema):
    number: str = Field(None, description="Số phụ lục hợp đồng")
    start_date: date = Field(None, description="Ngày bắt đầu")
    end_date: date = Field(None, description="Ngày kết thúc")


# Thông tin quyết định/hợp đồng
class ContractInfoResponse(BaseSchema):
    type: Optional[str] = Field(..., description="Loại hợp đồng")
    number: Optional[str] = Field(..., description="Số hợp đồng")
    start_date: Optional[date] = Field(..., description="Ngày bắt đầu")
    end_date: Optional[date] = Field(..., description="Ngày kết thúc")
    addendum: ContractAddendumResponse = Field(..., description="Số phụ lục hợp đồng")
    resign_date: date = Field(None, description="Ngày nghỉ việc")
