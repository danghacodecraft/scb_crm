from typing import Optional

from pydantic import Field
from pydantic.schema import datetime

from app.api.base.schema import BaseSchema


class DropdownResponse(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')
    code: str = Field(..., min_length=1, description='`Mã`')
    name: str = Field(..., min_length=1, description='`Tên`')


class OptionalDropdownResponse(BaseSchema):
    id: Optional[str] = Field(None, min_length=1, description='`Chuỗi định danh`', nullable=True)
    code: Optional[str] = Field(None, min_length=1, description='`Mã`', nullable=True)
    name: Optional[str] = Field(None, min_length=1, description='`Tên`', nullable=True)


class DropdownRequest(BaseSchema):
    id: str = Field(..., min_length=1, description='`Chuỗi định danh`')


class OptionalDropdownRequest(BaseSchema):
    id: Optional[str] = Field(None, min_length=1, description='`Chuỗi định danh`', nullable=True)


########################################################################################################################
# Response save
########################################################################################################################
class SaveSuccessResponse(BaseSchema):
    cif_id: str = Field(..., min_length=1, description='Id CIF ảo')
    booking_code: str = Field(..., min_length=1, description='Booking Code')


class HistoryData(BaseSchema):
    description: str = Field(..., description="Mô tả")
    created_at: datetime = Field(..., description="Bắt đầu lúc")
    completed_at: datetime = Field(..., description="Kết thúc lúc")
    status: int = Field(..., description="Trạng thái")
    branch_id: str = Field(..., description="Chi nhánh")
    branch_code: str = Field(..., description="Chi nhánh")
    branch_name: str = Field(..., description="Chi nhánh")
    user_id: str = Field(..., description="Mã NV")
    user_name: str = Field(..., description="Tên NV")
    position_id: str = Field(..., description="Chức vụ")
    position_code: str = Field(..., description="Chức vụ")
    position_name: str = Field(..., description="Chức vụ")
