from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class GWEmployeeInfoResponse(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")
    staff_name: str = Field(..., description="Tên nhân viên")
    fullname_vn: str = Field(..., description="Tên đầy đủ")
    work_location: str = Field(..., description="Địa điểm làm việc")
    email: str = Field(..., description="Địa chỉ email SCB")
    contact_mobile: str = Field(..., description="Điện thoại liên lạc")
    internal_mobile: str = Field(..., description="Điện thoại nội bộ")
    title_code: str = Field(..., description="Mã chức danh")
    title_name: str = Field(..., description="Tên chức danh")
    branch_org: List = Field(..., description="Cây đơn vị")
    avatar: str = Field(..., description="Hình ảnh đại diện nhân viên")
