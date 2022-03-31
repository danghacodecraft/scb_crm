from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin tuyển dụng
class RecruitInfoResponse(BaseSchema):
    recruitment_request_code: str = Field(..., description="Mã yêu cầu tuyển dụng")
    recruitment_reason: str = Field(..., description="Lý do tuyển dụng")
    people_introduce: str = Field(..., description="Người giới thiệu")
    replacement_staff: str = Field(..., description="Nhân viên thay thế")
    note: str = Field(None, description="Ghi chú tuyển dụng")


# Thông tin khác
class OtherInfoResponse(BaseSchema):
    other_info: str = Field(..., description="Thông tin khác")
    dateoff: str = Field(..., description="Tháng thâm niên cộng thêm")
    annual_leave: str = Field(..., description="Số phép năm ưu đãi")


# Thông tin phụ
class SubInfoResponse(BaseSchema):
    recruit_info: RecruitInfoResponse = Field(..., description="Thông tin tuyển dụng")
    other_info: OtherInfoResponse = Field(..., description="Thông tin khác")
