from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Đơn vị công tác hiện tại
class CurrentWorkingUnitResponse(BaseSchema):
    current_working_unit: DropdownResponse = Field(..., description="Đơn vị công tác hiện tại")
    company_position: DropdownResponse = Field(..., description="Chức danh")


# Đơn vị gốc
class OriginalUnitResponse(BaseSchema):
    original_unit: DropdownResponse = Field(..., description="Đơn vị gốc")
    company_position: DropdownResponse = Field(..., description="Chức danh")


# Đơn vị tạm thời
class TemporaryUnitResponse(BaseSchema):
    temporary_unit: DropdownResponse = Field(..., description="Đơn vị tạm thời")
    company_position: DropdownResponse = Field(..., description="Chức danh")


# Thông tin hồ sơ công tác
class WorkProfileInfoResponse(BaseSchema):
    working_day: str = Field(..., description="Ngày vào làm việc")
    probationary_day: str = Field(..., description="Ngày thử việc")
    official_date: str = Field(..., description="Ngày vào chính thức")
    current_unit: CurrentWorkingUnitResponse = Field(..., description="Đơn vị công tác hiện tại")
    root_unit: OriginalUnitResponse = Field(..., description="Đơn vị công gốc")
    temporary_unit: TemporaryUnitResponse = Field(..., description="Đơn vị tạm thời")
    seniority_date: date = Field(..., description="Ngày tính thâm niên")
    resident_object: bool = Field(..., description="Đối tượng cư trú")
