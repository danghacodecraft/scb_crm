from typing import Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema


class GWBranchDropdownResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã đơn vị")
    name: Optional[str] = Field(..., description="Tên đơn vị không dấu")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWCIFInfoResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="Số CIF")
    issued_date: Optional[str] = Field(..., description="Ngày cấp số CIF")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string
