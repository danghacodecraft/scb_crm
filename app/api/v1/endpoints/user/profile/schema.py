from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class ProfileResponse(BaseSchema):
    avatar: Optional[str] = Field(None, description='Avatar')
    gender: Optional[str] = Field(..., description="Giới tính")
    full_name_vn: Optional[str] = Field(..., description="Họ tên")
    email: Optional[str] = Field(..., description="Email")
    mobile_number: Optional[str] = Field(..., description="Điện thoại")
    code: Optional[str] = Field(..., description="Mã số nhân viên")
    department: Optional[str] = Field(..., description="Đơn vị công tác")
    titles: Optional[str] = Field(None, description="Chức danh")
    manager: Optional[str] = Field(None, description="Cấp quản lý trực tiếp")
    telephone_number: Optional[str] = Field(..., description="Số điện thoại nội bộ")
