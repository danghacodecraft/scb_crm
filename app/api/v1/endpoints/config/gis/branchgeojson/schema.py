from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class GeometryResponseResponse(BaseSchema):
    type: str = Field(..., description='`Loại geometry`')
    coordinates: List[float] = Field(..., description='`Coordinates`')


class PropertiesFeaturesResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh đơn vị`')
    name: str = Field(..., description='`Tên đơn vị`')
    code: str = Field(..., description='`Mã đơn vị`')
    address: str = Field(..., description='`Địa chỉ`')
    zone_id: str = Field(..., description='`Mã vùng`')
    zone_name: str = Field(..., description='`Tên vùng`')
    area_id: str = Field(..., description='`Mã khu vực`')
    area_name: str = Field(..., description='`Tên khu vực`')
    type: str = Field(..., description='`Loại tính chất`')


class FeaturesResponse(BaseSchema):
    id: str = Field(..., description="Mã đơn vị")
    type: str = Field(..., description="Loại features")
    properties: PropertiesFeaturesResponse = Field(..., description='`Tính chất`')
    geometry: GeometryResponseResponse = Field(..., description='`Geometry`')


class PropertiesResponse(BaseSchema):
    name: str = Field(..., description="Tên tính chất")


class CrsResponse(BaseSchema):
    type: str = Field(..., description='`Loại chi nhánh`')
    properties: PropertiesResponse = Field(..., description='`Tính chất`')


class BranchgeojsonResponse(BaseSchema):
    type: str = Field(..., description='`Loại chi nhánh`')
    crs: CrsResponse = Field(..., description='`Hệ quy chiếu tọa độ`')
    features: List[FeaturesResponse] = Field(..., description='`Features`')
