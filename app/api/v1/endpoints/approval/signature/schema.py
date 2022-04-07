from datetime import date
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


class CompareSignaturesResponse(BaseSchema):
    compare_image_url: str = Field(..., description='Hình ảnh đối chiếu')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class SignaturesSuccessResponse(BaseSchema):
    created_date: date = Field(..., description='Ngày tạo')
    signature: List[SignaturesResponse] = Field(..., description='Danh sách ảnh khuôn mặt')


class CompareSignatureRequest(BaseSchema):
    uuid_ekyc: str = Field(..., description='uuid_ekyc call upload file')
    uuid: str = Field(..., description='uuid call upload file')


class CompareSignatureResponse(BaseSchema):
    image_url: str = Field(..., description='url image')
    similarity_percent: int = Field(..., description='Tỷ lệ phần trăm giống nhau giữa hai hình ảnh')
