from datetime import datetime
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.functions import make_description_from_dict


class CreateBookingRequest(BaseSchema):
    business_type_code: str = Field(..., description=f"Loại nghiệp vụ: {make_description_from_dict(BUSINESS_TYPES)}")


class CreateBookingResponse(BaseSchema):
    booking_id: str = Field(..., description="Booking ID")
    booking_code: str = Field(..., description="Booking Code")


class NewsCommentResponse(BaseSchema):
    comment_id: str = Field(..., description="id tin tức")


class NewsCommentRequest(BaseSchema):
    content: str = Field(..., description='Nội dung comment')


class CommentResponse(BaseSchema):
    id: str = Field(..., description="ID comment")
    booking_id: str = Field(..., description="Booking ID")
    avatar_url: Optional[str] = Field(..., description="URL ảnh đại diện")
    username: str = Field(..., description="Username người comment")
    name: str = Field(..., description="Tên người comment")
    code: str = Field(..., description="Mã nhân viên người comment")
    email: str = Field(..., description="Email người comment")
    hrm_department_id: Optional[str] = Field(..., description="ID Phòng ban")
    hrm_department_code: Optional[str] = Field(..., description="Mã Phòng ban")
    hrm_department_name: Optional[str] = Field(..., description="Tên Phòng ban")
    hrm_branch_id: Optional[str] = Field(..., description="ID Chi nhánh/Hội sở người tạo comment")
    hrm_branch_code: Optional[str] = Field(..., description="Mã Chi nhánh/Hội sở")
    hrm_branch_name: Optional[str] = Field(..., description="Tên Chi nhánh/Hội sở")
    hrm_title_id: str = Field(..., description="ID Chức danh")
    hrm_title_code: str = Field(..., description="Mã Chức danh")
    hrm_title_name: str = Field(..., description="Tên Chức danh")
    hrm_position_id: Optional[str] = Field(..., description="ID Chức vụ")
    hrm_position_code: Optional[str] = Field(..., description="Mã Chức vụ")
    hrm_position_name: Optional[str] = Field(..., description="Tên Chức vụ")
    content: str = Field(..., description="Nội dung comment")
    created_at: Optional[datetime] = Field(..., description="Ngày tạo")
    updated_at: Optional[datetime] = Field(..., description="Ngày cập nhập")
    file_uuid: Optional[str] = Field(..., description="URL file đính kèm")


class StateResponse(BaseSchema):
    state_id: str = Field(..., description="id của trạng thái hồ sơ")


class StateReq(BaseSchema):
    state_id: str = Field(..., description="id của trạng thái hồ sơ")
    booking_id: str = Field(...)
