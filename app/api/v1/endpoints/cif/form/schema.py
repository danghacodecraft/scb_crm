from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


class ProcessInfoResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name_vn: str = Field(..., description="Tên đầy đủ của người dùng ")
    avatar_url: Optional[str] = Field(None, description="Url ảnh đại diện của người dùng")
    position: OptionalDropdownResponse = Field(..., description="Chức vụ")
    # id: str = Field(..., description="Id log")
    created_at: datetime = Field(..., description="Thời gian tạo")
    content: str = Field(..., description="Nội dung log ")


class CifApprovalProcessResponse(BaseSchema):
    created_at: date = Field(..., description="Ngày tạo")
    logs: List[ProcessInfoResponse] = Field(..., description="Danh sách log trong 1 ngày ")


class CifApproveRequest(BaseSchema):
    reject_flag: Optional[bool] = Field(None, description="Cờ từ chối phê duyệt")
    content: str = Field(..., description="Nội dung phê duyệt")


class CifApprovalResponse(BaseSchema):
    cif_id: str = Field(..., description="Cif ID")
    previous_stage: Optional[str] = Field(..., description="Bước trước đó")
    current_stage: str = Field(..., description="Bước hiện tại")
    next_stage: str = Field(..., description="Bước tiếp theo")


class CIFStageResponse(BaseSchema):
    stage_code: Optional[str] = Field(..., description="Mã bước giao dịch")
    is_disable: bool = Field(..., description="Có disable không")
    is_completed: bool = Field(..., description="Trạng thái phê duyệt")
    content: Optional[str] = Field(..., description="1. Nội dung phản hồi")
    action: Optional[str] = Field(None, description="2. Hành động")
    created_at: Optional[datetime] = Field(..., description="Cập nhật lúc")
    created_by: Optional[str] = Field(..., description="Cập nhật bởi")


class CifApprovalSuccessResponse(BaseSchema):
    cif_id: str = Field(..., description="Cif ID")
    stages: List[CIFStageResponse] = Field(..., description="Thông tin các bước phê duyệt")
