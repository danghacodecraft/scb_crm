from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, OptionalDropdownResponse


########################################################################################################################
# Response
########################################################################################################################
class OptionalAddressResponse(BaseSchema):
    province: OptionalDropdownResponse = Field(None, description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(None, description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(None, description="Phường/Xã")
    number_and_street: str = Field(None, description="Số nhà, tên đường")


# I. Thông tin cơ bản
class BasicInformationResponse(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    customer_relationship: OptionalDropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: Optional[str] = Field(..., description="Số ĐT bàn")
    mobile_number: Optional[str] = Field(..., description="Số ĐTDĐ")
    email: Optional[str] = Field(..., description="Email")


# II. Giấy tờ định danh
class IdentityDocumentResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


# III. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: OptionalAddressResponse = Field(..., description="Địa chỉ thường trú")
    contact_address: OptionalAddressResponse = Field(..., description="Địa chỉ liên hệ")


# Thông tin người giám hộ -> Danh sách người giám hộ
class GuardianResponse(BaseSchema):
    id: str = Field(..., description="ID người giám hộ")
    avatar_url: Optional[str] = Field(..., description="URL avatar người giám hộ")
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")


# Thông tin người giám hộ
class DetailGuardianResponse(BaseSchema):
    guardian_flag: bool = Field(..., description="Cờ có người giám hộ không")
    number_of_guardian: int = Field(..., description="Số người giám hộ")
    guardians: List[GuardianResponse] = Field(..., description="Danh sách người giám hộ")
    booking: OptionalDropdownResponse = Field(..., description="Booking")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin người giám hộ
class SaveGuardianRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
