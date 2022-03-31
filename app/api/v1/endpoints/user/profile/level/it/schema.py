from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin trình độ tin học
class LevelInformaticsInfoResponse(BaseSchema):
    certificate: str = Field(..., description="Chứng chỉ"),
    level: str = Field(..., description="Trình độ")
    point: str = Field(None, description="Điểm số/Xếp loại")
