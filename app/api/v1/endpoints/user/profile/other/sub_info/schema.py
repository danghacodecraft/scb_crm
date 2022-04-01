from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin tuyển dụng
class RecruitInfoResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã yêu cầu tuyển dụng")
    reason: Optional[str] = Field(..., description="Lý do tuyển dụng")
    introducer: Optional[str] = Field(..., description="Người giới thiệu")
    replacement_staff: Optional[str] = Field(..., description="Nhân viên thay thế")
    note: Optional[str] = Field(None, description="Ghi chú tuyển dụng")


# Thông tin khác
class OtherInfoResponse(BaseSchema):
    other_info: Optional[str] = Field(..., description="Thông tin khác")
    dateoff: Optional[str] = Field(..., description="Tháng thâm niên cộng thêm")
    annual_leave: Optional[str] = Field(..., description="Số phép năm ưu đãi")


# Thông tin phụ
class SubInfoResponse(BaseSchema):
    recruit_info: RecruitInfoResponse = Field(..., description="Thông tin tuyển dụng")
    other_info: OtherInfoResponse = Field(..., description="Thông tin khác")
