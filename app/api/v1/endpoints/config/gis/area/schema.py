from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class BranchsResponse(BaseSchema):
    branch_id: str = Field(..., description='`Mã khu vực`')
    branch_name: str = Field(..., description='`Tên khu vực`')
    longitude: float = Field(..., description='`Kinh độ địa lý`')
    latitude: float = Field(..., description='`Vĩ độ địa lý`')
    type: str = Field(..., description='`Loại khu vực`')


class AreaResponse(BaseSchema):
    ID: str = Field(..., description='`Mã khu vực`')
    NAME: str = Field(..., description='`Tên khu vực`')
    branches: List[BranchsResponse] = Field(..., description='`Chi nhánh`')
