from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, ResponseRequestSchema
from app.api.v1.schemas.utils import (
    OptionalDropdownRequest, OptionalDropdownResponse
)


class BookingAccountResponse(BaseSchema):
    booking_id: str = Field(..., description="Mã Booking Con")
    account_id: str = Field(..., description="Mã TKTT")


class SaveCasaSuccessResponse(BaseSchema):
    booking_parent_id: str = Field(..., description="Mã Booking Cha")
    booking_accounts: List[BookingAccountResponse] = Field(..., description="Danh sách các TKTT")


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: int = Field(..., description="Số lượng")


class SenderInfoRequest(BaseSchema):
    cif_number: Optional[str] = Field(None, description="Số CIF")
    full_name_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity_number: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: OptionalDropdownRequest = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_number: Optional[str] = Field(None, description="SĐT")


class SenderIdentityInfoResponse(BaseSchema):
    number: Optional[str] = Field(..., description="Số GTDD")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


# II. Thông tin khách hàng giao dịch
class SenderInfoResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="Mã khách hàng giao dịch")
    full_name_vn: Optional[str] = Field(..., description="Người giao dịch")
    identity_info: SenderIdentityInfoResponse = Field(..., description="Giấy tờ định danh")
    address_full: Optional[str] = Field(..., description="Địa chỉ")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại")
