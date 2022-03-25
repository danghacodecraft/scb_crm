from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class ApprovalTemplateInfoResponse(BaseSchema):
    id: str = Field(..., description="ID Biểu mẫu")
    name: str = Field(..., description="Tên Biểu mẫu")
    is_related_flag: bool = Field(..., description="Biểu mẫu có liên quan tới chương trình không")


class ApprovalFormResponse(BaseSchema):
    id: str = Field(..., description="ID thư mục")
    name: str = Field(..., description="Tên thư mục")
    templates: List[ApprovalTemplateInfoResponse] = Field(..., description="Danh sách biểu mẫu đi kèm thư mục")
