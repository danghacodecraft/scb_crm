from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, OptionalDropdownResponse


########################################################################################################################
# Response
########################################################################################################################
class AddressResponse(BaseSchema):
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường")


# I. Thông tin cơ bản
class BasicInformationResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="Số CIF")
    customer_relationship: OptionalDropdownResponse = Field(..., description="Mối quan hệ với khách hàng")
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    telephone_number: Optional[str] = Field(..., description="Số ĐT bàn", nullable=True)
    mobile_number: Optional[str] = Field(..., description="Số ĐTDĐ", nullable=True)
    email: Optional[str] = Field(..., description="Email", nullable=True)


# II. Giấy tờ định danh
class IdentityDocumentResponse(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


# III. Thông tin địa chỉ
class AddressInformationResponse(BaseSchema):
    resident_address: AddressResponse = Field(..., description="Địa chỉ thường trú")
    contact_address: AddressResponse = Field(..., description="Địa chỉ liên hệ")


# Thông tin mối quan hệ khách hàng -> Danh sách mối quan hệ khách hàng
class CustomerRelationshipResponse(BaseSchema):
    id: Optional[str] = Field(..., description="ID mối quan hệ khách hàng")
    avatar_url: Optional[str] = Field(..., description="URL avatar mối quan hệ khách hàng")
    basic_information: BasicInformationResponse = Field(..., description="I. Thông tin cơ bản")
    identity_document: IdentityDocumentResponse = Field(..., description="II. Giấy tờ định danh")
    address_information: AddressInformationResponse = Field(..., description="III. Thông tin địa chỉ")


# Thông tin mối quan hệ khách hàng
class DetailCustomerRelationshipResponse(BaseSchema):
    customer_relationship_flag: bool = Field(..., description="Cờ có người mối quan hệ khách hàng không")
    number_of_customer_relationship: int = Field(..., description="Số mối quan hệ khách hàng")
    relationships: List[CustomerRelationshipResponse] = Field(..., description="Danh sách mối quan hệ khách hàng")
    booking: OptionalDropdownResponse = Field(..., description="Booking")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin mối quan hệ khách hàng
class SaveCustomerRelationshipRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
