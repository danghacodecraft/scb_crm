from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


class ProfileResponse(BaseSchema):
    avatar: Optional[str] = Field(None, description='Avatar')
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    full_name_vn: Optional[str] = Field(..., description="Họ tên")
    user_name: Optional[str] = Field(..., description="User name")
    address: Optional[str] = Field(..., description="Địa chỉ")
    email: Optional[str] = Field(..., description="Email")
    mobile_number: Optional[str] = Field(..., description="Điện thoại")
    code: Optional[str] = Field(..., description="Mã số nhân viên")
    department: OptionalDropdownResponse = Field(..., description="Đơn vị công tác")
    title: OptionalDropdownResponse = Field(None, description="Chức danh")
    manager: Optional[str] = Field(None, description="Cấp quản lý trực tiếp")
    telephone_number: Optional[str] = Field(..., description="Số điện thoại nội bộ")
