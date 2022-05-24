from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


class GWCategoryRequest(BaseSchema):
    transaction_name: str = Field(...)
    transaction_value: List = Field([])


class CategoryRequest(BaseSchema):
    employee_code: str = Field(..., description="Mã nhân viên")
    employee_name: str = Field(..., description="Tên nhân viên")
    department: OptionalDropdownResponse = Field(..., description="Phòng ban")
    unit_code: OptionalDropdownResponse = Field(..., description="Mã đơn vị")
