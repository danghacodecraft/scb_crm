from typing import List

from fastapi import Depends, File, Form, Path, UploadFile
from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.dependencies.authenticate import get_current_user_from_header


class ApprovalCompareFaceImageUrls(BaseSchema):
    url: str = Field(..., description="Link hình ảnh")
    similar_percent: int = Field(..., description="Tỉ lệ chính xác của hình hiện tại so với `face_url`")


class ApprovalFaceSuccessResponse(BaseSchema):
    cif_id: str = Field(..., description='Id CIF ảo')
    face_url: str = Field(..., description='Id CIF ảo')
    compare_face_image_urls: List[ApprovalCompareFaceImageUrls] = Field(..., description='Danh sách hình ảnh so sánh')


class ApprovalFaceRequest(BaseSchema):
    @staticmethod
    def get_upload_request(
            cif_id: str = Path(..., description='Id CIF ảo'),
            image_file: UploadFile = File(...),
            amount: int = Form(2, description="Số lượng hình ảnh so sánh"),
            current_user=Depends(get_current_user_from_header()),
    ):
        return cif_id, image_file, amount, current_user
