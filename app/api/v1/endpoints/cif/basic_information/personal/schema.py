from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownResponse
)


class ContactMethodRequest(BaseSchema):
    email_flag: bool = Field(False, description='Email. `True`: Là chọn. `False`: Không chọn')
    mobile_number_flag: bool = Field(False, description='Di động. `True`: Là chọn. `False`: Không chọn')


class PersonalRequest(BaseSchema):
    full_name_vn: str = Field(..., description='Tên tiếng việt của khách hàng')
    gender: DropdownRequest = Field(..., description='Giới tính khách hàng')
    honorific: DropdownRequest = Field(..., description='Danh xưng khách hàng')
    date_of_birth: date = Field(..., description='Ngày sinh khách hàng')
    under_15_year_old_flag: bool = Field(False, description='Trạng thái dưới 15 tuổi')
    place_of_birth: DropdownRequest = Field(..., description='Nơi sinh khách hàng')
    country_of_birth: DropdownRequest = Field(..., description='Quốc gia sinh khách hàng')
    nationality: DropdownRequest = Field(..., description='Quốc tịch khách hàng')
    tax_number: str = Field(None, description='Mã số thuế cá nhân của khách hàng')
    resident_status: DropdownRequest = Field(..., description='Tình trạng cư trú khách hàng')
    mobile_number: Optional[str] = Field(None, description='Điện thoại di động khách hàng')
    telephone_number: str = Field(None, description='Điện thoại bàn khách hàng')
    email: str = Field(None, description='Email khách hàng')
    contact_method: ContactMethodRequest = Field(..., description='Hình thức liên hệ khách hàng')
    marital_status: DropdownRequest = Field(None, description='Tình trạng hôn nhân khách hàng')


class ContactMethodResponse(BaseSchema):
    email_flag: bool = Field(..., description='Email. `True`: Chọn. `False`: Không chọn')
    mobile_number_flag: bool = Field(..., description='Di động. `True`: Chọn. `False`: Không chọn')


class PersonalResponse(BaseSchema):
    full_name_vn: str = Field(..., description='Tên tiếng việt khách hàng')
    gender: DropdownResponse = Field(..., description='Giới tính khách hàng')
    honorific: DropdownResponse = Field(..., description='Danh xưng khách hàng')
    date_of_birth: date = Field(..., description='Ngày sinh khách hàng')
    under_15_year_old_flag: bool = Field(..., description='Trạng thái dưới 15 tuổi')
    place_of_birth: DropdownResponse = Field(..., description='Nơi sinh khách hàng')
    country_of_birth: DropdownResponse = Field(..., description='Quốc gia sinh khách hàng')
    nationality: DropdownResponse = Field(..., description='Quốc tịch khách hàng')
    tax_number: Optional[str] = Field(..., description='Mã số thuế cá nhân của khách hàng', nullable=True)
    resident_status: DropdownResponse = Field(..., description='Tình trạng cư trú khách hàng')
    mobile_number: Optional[str] = Field(..., description='Điện thoại di động khách hàng')
    telephone_number: Optional[str] = Field(..., description='Điện thoại bàn khách hàng', nullable=True)
    email: Optional[str] = Field(..., description='Email khách hàng', nullable=True)
    contact_method: ContactMethodResponse = Field(..., description='Hình thức liên hệ khách hàng')
    marital_status: OptionalDropdownResponse = Field(..., description='Tình trạng hôn nhân khách hàng')
