from datetime import datetime
from typing import List, Optional

from fastapi import Form
from pydantic import Field

from app.api.base.schema import BaseSchema


class ApprovalSignatureImageUrls(BaseSchema):
    url: str = Field(..., description="Link hình ảnh")
    similar_percent: int = Field(..., description="Tỉ lệ chính xác của hình hiện tại so với `signature_url`")


class ApprovalSignatureSuccessResponse(BaseSchema):
    cif_id: Optional[str] = Field(..., description='Id CIF ảo')
    compare_signature_image_url: Optional[str] = Field(..., description='URL chữ ký upload')
    compare_signature_image_uuid: Optional[str] = Field(..., description='UUID chữ ký upload')
    created_at: datetime = Field(..., description='Thời gian tạo')
    signature_image_urls: List[ApprovalSignatureImageUrls] = Field(..., description='Danh sách hình ảnh so sánh')


class ApprovalSignatureRequest(BaseSchema):
    compare_uuid: str = Field(..., description="UUID hình ảnh cần upload")
    compare_uuid_ekyc: str = Field(..., description="UUID ekyc hình ảnh cần upload")
    amount: int = Form(2, description="Số lượng hình ảnh so sánh")
