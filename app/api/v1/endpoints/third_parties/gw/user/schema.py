from pydantic import Field

from app.api.base.schema import BaseSchema


class StaffInfoUserResponse(BaseSchema):
    full_name: str = Field(..., description="Tên đầy đủ của nhân viên")
    title_name: str = Field(..., description="Chức danh")
    staff_code: str = Field(..., description="Mã nhân viên")


class BranchInfoUserResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị")
    branch_name: str = Field(..., description="Tên đơn vị")


class GWDetailUserInfoResponse(BaseSchema):
    user_code: str = Field(..., description="UserID")
    staff_info: StaffInfoUserResponse = Field(...)
    branch_info: BranchInfoUserResponse = Field(...)
    current_date: str = Field(..., description="Ngày giao dịch trên hệ thống")
