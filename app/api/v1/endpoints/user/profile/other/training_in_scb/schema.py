from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình đào tạo trong ngân hàng
class TrainingInSCBResponse(BaseSchema):
    topic: str = Field(..., description="Chủ đề")
    course_code: str = Field(None, description="Mã khóa học")
    course_name: str = Field(None, description="Tên khóa học")
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")
    result: str = Field(..., description="Kết quả")
