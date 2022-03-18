from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class ApprovalCompareFaceImageUrls(BaseSchema):
    url: str = Field(..., description="Link hình ảnh")
    similar_percent: int = Field(..., description="Tỉ lệ chính xác của hình hiện tại so với `face_url`")


class ApprovalFaceSuccess(BaseSchema):
    cif_id: str = Field(..., description='Id CIF ảo')
    face_url: str = Field(..., description='Id CIF ảo')
    compare_face_image_urls: List[ApprovalCompareFaceImageUrls] = Field(..., description='Danh sách hình ảnh so sánh')
