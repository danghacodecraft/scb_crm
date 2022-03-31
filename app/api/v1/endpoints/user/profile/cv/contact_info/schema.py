from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


# Nguyên quán
class DomicileResponse(BaseSchema):
    domicile: str = Field(..., description="Nguyên quán")
    nationality: DropdownResponse = Field(..., description="Quốc gia")
    province: DropdownResponse = Field(..., description="Tỉnh/TP")
    district: DropdownResponse = Field(..., description="Quận/huyên")
    ward: DropdownResponse = Field(..., description="Phường/xã")


# Thường trú
class ResidentResponse(BaseSchema):
    resident_address: str = Field(..., description="Địa chỉ thường trú")
    nationality: DropdownResponse = Field(..., description="Quốc gia")
    province: DropdownResponse = Field(..., description="Tỉnh/TP")
    district: DropdownResponse = Field(..., description="Quận/huyên")
    ward: DropdownResponse = Field(..., description="Phường/xã")


# Tạm trú
class TemporaryResidenceResponse(BaseSchema):
    temporary_residence_address: str = Field(..., description="Địa chỉ tạm trú")
    nationality: DropdownResponse = Field(..., description="Quốc gia")
    province: DropdownResponse = Field(..., description="Tỉnh/TP")
    district: DropdownResponse = Field(..., description="Quận/huyên")
    ward: DropdownResponse = Field(..., description="Phường/xã")


# Liên lạc
class ContactResponResponse(BaseSchema):
    resident_address: str = Field(..., description="Địa chỉ thường trú")
    nationality: DropdownResponse = Field(..., description="Quốc gia")
    province: DropdownResponse = Field(..., description="Tỉnh/TP")
    district: DropdownResponse = Field(..., description="Quận/huyên")
    ward: DropdownResponse = Field(..., description="Phường/xã")


# Thông tin liên hệ
class ContactInfoResponse(BaseSchema):
    domicile: DomicileResponse = Field(..., description="Nguyên quán")
    resident: ResidentResponse = Field(..., description="Thường trú")
    temporary_residence: TemporaryResidenceResponse = Field(..., description="Tạm trú")
    contact: ContactResponResponse = Field(..., description="Liên lạc")


# Người liên hệ
class ContactResponse(BaseSchema):
    contact: str = Field(..., description="Người liên hệ")
    relationship: DropdownResponse = Field(..., description="Quan hệ")
    mobile_num: str = Field(..., description="Số điện thoại")


# Người bảo lãnh
class GuardianResponse(BaseSchema):
    guardian: str = Field(..., description="Người bảo lãnh")
    relationship: DropdownResponse = Field(..., description="Quan hệ")
    mobile_num: str = Field(..., description="Số điện thoại")


# Thông tin khác
class OtherInfoResponse(BaseSchema):
    contact: ContactResponse = Field(..., description="Người liên hệ")
    guardian: GuardianResponse = Field(..., description="Người bảo lãnh")
    expiration_date: date = Field(..., description="Ngày hết hiệu lực")


# Thông tin liên hệ nhân viên
class EmployeeInfoResponse(BaseSchema):
    contact_info: ContactInfoResponse = Field(..., description="Thông tin liên hệ")
    other_info: OtherInfoResponse = Field(..., description="Thông tin khác")
