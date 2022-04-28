from pydantic import Field

from app.api.base.schema import BaseSchema


class BranchResponse(BaseSchema):
    region_id: str = Field(..., description="Mã vùng")
    region_name: str = Field(..., description="Tên vùng")
    area_id: str = Field(..., description="Mã khu vực")
    area_name: str = Field(..., description="Tên khu vực")
    branch_id: str = Field(..., description="Mã chi nhánh")
    branch_name: str = Field(..., description="Tên chi nhánh")
    longitude: float = Field(..., description='`Kinh độ địa lý`')
    latitude: float = Field(..., description='`Vĩ độ địa lý`')
    type: str = Field(..., description="Loại chi nhánh")
