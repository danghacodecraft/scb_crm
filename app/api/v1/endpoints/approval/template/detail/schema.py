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
