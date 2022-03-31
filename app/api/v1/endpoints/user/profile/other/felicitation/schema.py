from pydantic import Field

from app.api.base.schema import BaseSchema


class FelicitionResponse(BaseSchema):
    effective_date: str = Field(None, description="Ngày hiệu lực")
    decision_number: str = Field(None, description="Số quyết định")
    titles: str = Field(None, description="Danh hiệu")
    rank_commend: str = Field(None, description="Cấp khen thưởng")
    job_title_name: str = Field(None, description="Chức danh")
    dep_name: str = Field(None, description="Đơn vị/Phòng ban")
    reason_commend: str = Field(None, description="Lý do khen thưởng")
    form_commend: str = Field(None, description="Hình thức khen thưởng")
    bonus_amount: str = Field(None, description="Số tiền khen thưởng")
    sign_day: str = Field(None, description="Ngày ký")
    signer: str = Field(None, description="Người ký")
