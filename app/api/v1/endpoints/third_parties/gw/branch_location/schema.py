from pydantic import Field

from app.api.base.schema import BaseSchema


class SelectBranchesByRegionIdRequest(BaseSchema):
    region_id: str = Field(..., description="Mã vùng")


class SelectBranchesByRegionIdResponse(BaseSchema):
    region_id: str = Field(..., description="Mã vùng")
    region_name: str = Field(..., description="Tên vùng")
    area_id: str = Field(..., description="Tên khu vự")
    area_name: str = Field(..., description="Tên khu vự")
    branch_console: str = Field(...)
    branch_console_name: str = Field(...)
    branch_id: str = Field(..., description="Mã đơn vị")
    branch_name: str = Field(..., description="Tên đơn vị")
    latitude: float = Field(..., description="Vĩ độ")
    longtitude: float = Field(..., description="Kinh độ")
    region_type: str = Field(..., description="Loại đơn vị")
