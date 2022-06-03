from pydantic import Field

from app.api.base.schema import BaseSchema


class NewsDocumentFileResponse(BaseSchema):
    id: str = Field(..., description="id tin tức")
