from pydantic import Field

from app.api.base.schema import BaseSchema


class GWBranchDropdownResponse(BaseSchema):
    code: str = Field(..., description="Mã đơn vị")
    name: str = Field(..., description="Tên đơn vị không dấu")


class GWCIFInfoResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    issued_date: str = Field(..., description="Ngày cấp số CIF")
