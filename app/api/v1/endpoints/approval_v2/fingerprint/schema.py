from datetime import datetime
from typing import List, Optional

from fastapi import Form
from pydantic import Field

from app.api.base.schema import BaseSchema


class ApprovalFingerprintImageUrls(BaseSchema):
    url: str = Field(..., description="Link hình ảnh")
    similar_percent: int = Field(..., description="Tỉ lệ chính xác của hình hiện tại so với `fingerprint_url`")


class ApprovalFingerprintSuccessResponse(BaseSchema):
    cif_id: Optional[str] = Field(..., description='Id CIF ảo')
    compare_fingerprint_image_url: Optional[str] = Field(..., description='URL vân tay upload')
    compare_fingerprint_image_uuid: Optional[str] = Field(..., description='UUID vân tay upload')
    created_at: datetime = Field(..., description='Thời gian tạo')
    fingerprint_image_urls: List[ApprovalFingerprintImageUrls] = Field(..., description='Danh sách hình ảnh so sánh')


class ApprovalFingerprintRequest(BaseSchema):
    compare_uuid: str = Field(..., description="UUID hình ảnh cần upload")
    compare_uuid_ekyc: str = Field(..., description="UUID ekyc hình ảnh cần upload")
    amount: int = Form(2, description="Số lượng hình ảnh so sánh")
