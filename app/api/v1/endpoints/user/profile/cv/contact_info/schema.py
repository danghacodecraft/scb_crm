from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


# Nguyên quán
# Thường trú
# Tạm trú
# Liên lạc
class ContactResponse(BaseSchema):
    number_and_street: Optional[str] = Field(..., description="Nguyên quán")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc gia")
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/TP")
    district: OptionalDropdownResponse = Field(..., description="Quận/huyên")
    ward: OptionalDropdownResponse = Field(..., description="Phường/xã")


# Thông tin liên hệ
class ContactInfoResponse(BaseSchema):
    domicile: ContactResponse = Field(..., description="Nguyên quán")
    resident: ContactResponse = Field(..., description="Thường trú")
    temporary: ContactResponse = Field(..., description="Tạm trú")
    contact: ContactResponse = Field(..., description="Liên lạc")


class CommonContactor(BaseSchema):
    relationship: OptionalDropdownResponse = Field(..., description="Quan hệ")
    mobile_number: Optional[str] = Field(..., description="Số điện thoại")


# Người liên hệ
class ContactorResponse(CommonContactor):
    contactor: Optional[str] = Field(..., description="Người liên hệ")


# Người bảo lãnh
class GuardianResponse(CommonContactor):
    guardian: Optional[str] = Field(..., description="Người bảo lãnh")


# Thông tin khác
class OtherInfoResponse(BaseSchema):
    contact: ContactorResponse = Field(..., description="Người liên hệ")
    guardian: GuardianResponse = Field(..., description="Người bảo lãnh")
    expiration_date: Optional[date] = Field(..., description="Ngày hết hiệu lực")


# Thông tin liên hệ nhân viên
class EmployeeContactInfoResponse(BaseSchema):
    contact_info: ContactInfoResponse = Field(..., description="Thông tin liên hệ")
    other_info: OtherInfoResponse = Field(..., description="Thông tin khác")
