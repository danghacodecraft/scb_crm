from datetime import date

from pydantic import Field

from app.api.base.schema import BaseSchema
# Thông tin cá nhân
from app.api.v1.schemas.utils import DropdownResponse


class PersonalInfoResponse(BaseSchema):
    date_of_birth: date = Field(..., description="Ngày sinh")
    place_of_birth: DropdownResponse = Field(..., description="Nơi sinh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    ethnic: str = Field(..., description="Dân tộc")
    religion: str = Field(..., description="Tôn giáo")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    marital_status: bool = Field(..., description="Tình trạng hôn nhân")
    identity_num: str = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: date = Field(..., description="Ngày cấp")
    expiration_date: date = Field(None, description="Ngày hết hạn")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
