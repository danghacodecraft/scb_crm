from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình kỷ luật
class DisciplineResponse(BaseSchema):
    effective_date: Optional[date] = Field(..., description="Ngày hiệu lực")
    end_date: Optional[date] = Field(..., description="Ngày kết thúc")
    titles: Optional[str] = Field(..., description="Chức danh")
    department: Optional[str] = Field(..., description="Đơn vị/Phòng ban")
    reason: Optional[str] = Field(..., description="Lý do kỷ luật")
    detailed_reason: Optional[str] = Field(..., description="Lý do chi tiết")
    detected_date: Optional[str] = Field(..., description="Ngày phát hiện")
    violation_date: Optional[str] = Field(..., description="Ngày vi phạm")
    total_damage: Optional[str] = Field(..., description="Tổng giá trị thiệt hại")
    number: Optional[str] = Field(..., description="Số quyết định")
    deleter: Optional[str] = Field(..., description="Người xóa kỷ luật")
    signer: Optional[str] = Field(..., description="Người ký")
