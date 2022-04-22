from datetime import date, datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class SignatureRequest(BaseSchema):
    image_url: str = Field(..., description='Đường dẫn hình ảnh định danh chữ ký khách hàng')
    uuid_ekyc: str = Field(..., description='uuid_ekyc call upload file')


class SignaturesRequest(BaseSchema):
    signatures: List[SignatureRequest] = Field(..., description='Hình ảnh chữ ký')


class SignaturesResponse(BaseSchema):
    identity_image_id: str = Field(..., description='Mã hình ảnh chữ ký của khách hàng')
    image_url: str = Field(..., description='Hình ảnh chữ ký của khách hàng')
    active_flag: bool = Field(..., description='Trạng thái hoạt động')
    maker_at: datetime = Field(..., description='Thời gian')


class CompareSignaturesResponse(BaseSchema):
    compare_image_url: str = Field(..., description='Hình ảnh đối chiếu')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class SignaturesSuccessResponse(BaseSchema):
    created_date: date = Field(..., description='Ngày tạo')
    signature: List[SignaturesResponse] = Field(..., description='Danh sách ảnh khuôn mặt')
