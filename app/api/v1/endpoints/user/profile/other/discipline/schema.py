from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình kỷ luật
class DisciplineResponse(BaseSchema):
    effective_date: Optional[date] = Field(None, description="Ngày hiệu lực")
    end_date: Optional[date] = Field(None, description="Ngày kết thúc")
    titles: Optional[str] = Field(None, description="Chức danh")
    department: Optional[str] = Field(None, description="Đơn vị/Phòng ban")
    reasons: Optional[str] = Field(None, description="Lý do kỷ luật")
    detailed_reason: Optional[str] = Field(None, description="Lý do chi tiết")
    detected_date: Optional[str] = Field(None, description="Ngày phát hiện")
    violation_date: Optional[str] = Field(None, description="Ngày vi phạm")
    total_damage: Optional[str] = Field(None, description="Tổng giá trị thiệt hại")
    number: Optional[str] = Field(None, description="Số quyết định")
    deleter: Optional[str] = Field(None, description="Người xóa kỷ luật")
    signer: Optional[str] = Field(None, description="Người ký")
