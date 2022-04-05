from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình đào tạo trong ngân hàng
class KpiResponse(BaseSchema):
    assessment_period: Optional[str] = Field(..., description="Kỳ đánh giá")
    total_score: Optional[str] = Field(..., description="Tổng điểm KPIs")
    completion_rate: Optional[str] = Field(..., description="Tỷ lệ hoàn thành")
    result: Optional[str] = Field(..., description="Kết quả/Xếp hạng")
    note: Optional[str] = Field(None, description="Note")
