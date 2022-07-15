from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseGWSchema, BaseSchema


class SelectBranchByRegionIdRequest(BaseSchema):
    region_id: str = Field(..., description="Mã vùng")


class SelectBranchByBranchIdRequest(BaseSchema):
    branch_id: str = Field(..., description="Mã vùng")


class SelectBranchByRegionIdItemResponse(BaseGWSchema):
    branch_id: Optional[str] = Field(..., description="Mã đơn vị")
    branch_name: Optional[str] = Field(..., description="Tên đơn vị")
    latitude: Optional[float] = Field(..., description="Vĩ độ")
    longitude: Optional[float] = Field(..., description="Kinh độ")
    type: Optional[str] = Field(..., description="Loại đơn vị")


class SelectBranchByRegionIdResponse(BaseGWSchema):
    region_id: Optional[str] = Field(..., description="Mã vùng")
    region_name: Optional[str] = Field(..., description="Tên vùng")
    branches: List[SelectBranchByRegionIdItemResponse] = Field(..., description="Danh sách chi nhánh")
    left: Optional[float] = Field(..., description="Left location")
    right: Optional[float] = Field(..., description="Right location")
    top: Optional[float] = Field(..., description="Top location")
    bottom: Optional[float] = Field(..., description="Bottom location")


class SelectBranchByBranchIdResponse(BaseGWSchema):
    region_id: Optional[str] = Field(..., description="Mã vùng")
    region_name: Optional[str] = Field(..., description="Tên vùng")
    branch_id: Optional[str] = Field(..., description="Mã đơn vị")
    branch_name: Optional[str] = Field(..., description="Tên đơn vị")
    latitude: Optional[float] = Field(..., description="Vĩ độ")
    longitude: Optional[float] = Field(..., description="Kinh độ")
    type: Optional[str] = Field(..., description="Loại đơn vị")
