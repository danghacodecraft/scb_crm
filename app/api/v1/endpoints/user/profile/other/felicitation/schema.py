from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class FelicitationResponse(BaseSchema):
    effective_date: Optional[date] = Field(None, description="Ngày hiệu lực")
    decision_number: Optional[str] = Field(None, description="Số quyết định")
    titles: Optional[str] = Field(None, description="Danh hiệu")
    commend_level: Optional[str] = Field(None, description="Cấp khen thưởng")
    title: Optional[str] = Field(None, description="Chức danh")
    department: Optional[str] = Field(None, description="Đơn vị/Phòng ban")
    reason: Optional[str] = Field(None, description="Lý do khen thưởng")
    formality: Optional[str] = Field(None, description="Hình thức khen thưởng")
    amount: Optional[str] = Field(None, description="Số tiền khen thưởng")
    sign_date: Optional[date] = Field(None, description="Ngày ký")
    signer: Optional[str] = Field(None, description="Người ký")
