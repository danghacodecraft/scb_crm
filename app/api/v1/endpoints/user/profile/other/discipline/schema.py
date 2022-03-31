from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema


# Quá trình kỷ luật
class DiscriplineResponse(BaseSchema):
    effective_date: date = Field(None, description="Ngày hiệu lực")
    end_date: date = Field(None, description="Ngày kết thúc")
    titles: str = Field(None, description="Chức danh")
    dep_name: str = Field(None, description="Đơn vị/Phòng ban")
    disciplinary_reasons: str = Field(None, description="Lý do kỷ luật")
    detailed_reason: str = Field(None, description="Lý do chi tiết")
    date_detect: date = Field(None, description="Ngày phát hiện")
    date_violation: date = Field(None, description="Ngày vi phạm")
    total_damage_value: str = Field(None, description="Tổng giá trị thiệt hại")
    decision_number: str = Field(None, description="Số quyết định")
    people_delete_discipline: str = Field(None, description="Người xóa kỷ luật")
    signer: str = Field(None, description="Người ký")
