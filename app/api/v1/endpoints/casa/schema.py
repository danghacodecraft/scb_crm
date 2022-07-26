from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, ResponseRequestSchema
from app.api.v1.schemas.utils import OptionalDropdownRequest
from app.utils.constant.casa import DENOMINATIONS__AMOUNTS
from app.utils.functions import make_description_from_dict_to_list


class BookingAccountResponse(BaseSchema):
    booking_id: str = Field(..., description="Mã Booking Con")
    account_id: str = Field(..., description="Mã TKTT")


class SaveCasaSuccessResponse(BaseSchema):
    booking_parent_id: str = Field(..., description="Mã Booking Cha")
    booking_accounts: List[BookingAccountResponse] = Field(..., description="Danh sách các TKTT")


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")


class SenderInfoRequest(BaseSchema):
    cif_number: Optional[str] = Field(None, description="Số CIF")
    full_name_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity_number: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: OptionalDropdownRequest = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_number: Optional[str] = Field(None, description="SĐT")
