from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import OptionalDropdownResponse


# Thông tin cá nhân
class PersonalInfoResponse(BaseSchema):
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    place_of_birth: OptionalDropdownResponse = Field(..., description="Nơi sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    ethnic: OptionalDropdownResponse = Field(..., description="Dân tộc")
    religion: OptionalDropdownResponse = Field(..., description="Tôn giáo")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    marital_status: OptionalDropdownResponse = Field(..., description="Tình trạng hôn nhân")
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(None, description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")
