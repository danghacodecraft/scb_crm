from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


# Đơn vị công tác hiện tại
# Đơn vị gốc
# Đơn vị tạm thời
class WorkingProfileResponse(BaseSchema):
    branch: OptionalDropdownResponse = Field(..., description="Đơn vị tạm thời")
    position: OptionalDropdownResponse = Field(..., description="Chức danh")


# Thông tin hồ sơ công tác
class WorkProfileInfoResponse(BaseSchema):
    working_date: Optional[date] = Field(..., description="Ngày vào làm việc")
    probationary_date: Optional[date] = Field(..., description="Ngày thử việc")
    official_date: Optional[date] = Field(..., description="Ngày vào chính thức")
    current: WorkingProfileResponse = Field(..., description="Đơn vị công tác hiện tại")
    root: WorkingProfileResponse = Field(..., description="Đơn vị công gốc")
    temporary: WorkingProfileResponse = Field(..., description="Đơn vị tạm thời")
    seniority_date: Optional[date] = Field(..., description="Ngày tính thâm niên")
    is_resident: bool = Field(..., description="Đối tượng cư trú")
