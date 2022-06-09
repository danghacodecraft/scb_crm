from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class BookingAccountResponse(BaseSchema):
    booking_id: str = Field(..., description="Mã Booking Con")
    account_id: str = Field(..., description="Mã TKTT")


class SaveCasaSuccessResponse(BaseSchema):
    booking_parent_id: str = Field(..., description="Mã Booking Cha")
    booking_accounts: List[BookingAccountResponse] = Field(..., description="Danh sách các TKTT")
