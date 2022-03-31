from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình đào tạo trong ngân hàng
class KpiResponse(BaseSchema):
    assessment_period: str = Field(..., description="Kỳ đánh giá")
    total_score_kpis: str = Field(..., description="Tổng điểm KPIs")
    completion_rate: str = Field(..., description="Tỷ lệ hoàn thành")
    result: str = Field(..., description="Kết quả/Xếp hạng")
    note: str = Field(None, description="Note")
