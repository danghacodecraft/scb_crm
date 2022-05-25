from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class GWBranchDropdownResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã đơn vị")
    name: Optional[str] = Field(..., description="Tên đơn vị không dấu")


class GWCIFInfoResponse(BaseSchema):
    cif_number: Optional[str] = Field(..., description="Số CIF")
    issued_date: Optional[str] = Field(..., description="Ngày cấp số CIF")
