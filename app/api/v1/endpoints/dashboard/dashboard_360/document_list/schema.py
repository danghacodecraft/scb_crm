from datetime import datetime

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class DocumentListResponse(BaseSchema):
    created_by: str = Field(..., description="Tên người khởi tạo")
    file_uuid: str = Field(..., description="UUID của file")
    file_name: str = Field(..., description="Tên file")
    create_at: datetime = Field(..., description="Thời gian khởi tạo")
    file_type: DropdownResponse = Field(..., description="Kiểu file dữ liệu")
    # file_size: float = Field(..., description="Size")  # todo
