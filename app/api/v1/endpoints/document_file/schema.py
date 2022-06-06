from pydantic import Field

from app.api.base.schema import BaseSchema


class DocumentFileResponse(BaseSchema):
    id: str = Field(..., description="id file tài liệu")
