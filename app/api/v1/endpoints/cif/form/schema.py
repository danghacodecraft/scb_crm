from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class ProcessInfoResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name: str = Field(..., description="Tên đầy đủ của người dùng ")
    user_avatar_url: str = Field(..., description="Url ảnh đại diện của người dùng")
    id: str = Field(..., description="Id log")
    created_at: datetime = Field(..., description="Thời gian tạo")
    content: str = Field(..., description="Nội dung log ")


class CifApprovalProcessResponse(BaseSchema):
    created_date: str = Field(..., description="Ngày tạo")
    logs: List[ProcessInfoResponse] = Field(..., description="Danh sách log trong 1 ngày ")
