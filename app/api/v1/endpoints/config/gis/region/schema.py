from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class BranchsResponse(BaseSchema):
    branch_id: str = Field(..., description='`Mã chi nhánh`')
    branch_name: str = Field(..., description='`Tên chi nhánh`')
    longitude: float = Field(..., description='`Kinh độ địa lý`')
    latitude: float = Field(..., description='`Vĩ độ địa lý`')
    type: str = Field(..., description='`Loại chi nhánh`')


class RegionResponse(BaseSchema):
    region_id: str = Field(..., description='`Mã vùng`')
    region_name: str = Field(..., description='`Tên vùng`')
    branches: List[BranchsResponse] = Field(..., description='`Chi nhánh`')
