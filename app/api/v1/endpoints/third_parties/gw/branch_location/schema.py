from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseGWSchema, BaseSchema


class SelectBranchByRegionIdRequest(BaseSchema):
    region_id: str = Field(..., description="Mã vùng")


class SelectBranchByBranchIdRequest(BaseSchema):
    branch_id: str = Field(..., description="Mã vùng")


class SelectBranchByRegionIdItemResponse(BaseGWSchema):
    area_id: Optional[str] = Field(..., description="Tên khu vự")
    area_name: Optional[str] = Field(..., description="Tên khu vự")
    branch_console: Optional[str] = Field(...)
    branch_console_name: Optional[str] = Field(...)
    branch_id: Optional[str] = Field(..., description="Mã đơn vị")
    branch_name: Optional[str] = Field(..., description="Tên đơn vị")
    latitude: Optional[float] = Field(..., description="Vĩ độ")
    longtitude: Optional[float] = Field(..., description="Kinh độ")
    region_type: Optional[str] = Field(..., description="Loại đơn vị")


class SelectBranchByRegionIdResponse(BaseGWSchema):
    region_id: Optional[str] = Field(..., description="Mã vùng")
    region_name: Optional[str] = Field(..., description="Tên vùng")
    branches: List = Field(..., description="Danh sách chi nhánh")
