from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Số phụ lục hợp đồng
class ContractAppendixResponse(BaseSchema):
    number: str = Field(None, description="Số phụ lục hợp đồng")
    start_day: date = Field(None, description="Ngày bắt đầu")
    end_day: date = Field(None, description="Ngày kết thúc")


# Thông tin quyết định/hợp đồng
class DecisionContractInfoResponse(BaseSchema):
    type: DropdownResponse = Field(..., description="Loại hợp đồng")
    number: str = Field(..., description="Số hợp đồng")
    start_day: date = Field(..., description="Ngày bắt đầu")
    end_day: date = Field(None, description="Ngày kết thúc")
    contract_addendum: ContractAppendixResponse = Field(..., description="Số phụ lục hợp đồng")
    date_resign: date = Field(None, description="Ngày nghỉ việc")
