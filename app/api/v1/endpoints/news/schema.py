from typing import Optional

from fastapi import File, UploadFile
from pydantic import Field

from app.api.base.schema import BaseSchema


class NewsRequest(BaseSchema):
    tilte: str = Field(..., description='Tiêu đề')
    news_category_id: str = Field(..., description='Loại tin')
    user_id: str = Field(..., description='user_id')
    user_name: Optional[str] = Field(..., description='Tên người tạo')
    content: str = Field(None, description="Nội dung")
    summary: str = Field(None, description="Tóm tắt nội dung")
    start_date: str = Field(..., description="Ngày bắt đầu")
    expired_date: str = Field(None, description="Ngày kết thúc")
    active_flag: str = Field(..., description="Trạng thái kích hoạt")


class NewsResponse(BaseSchema):
    tilte: str = Field(None, description='Tiêu đề')
    avatar_url: str = Field(None, description='Đường dẫn avatar')
    thumbnail_url: str = Field(None, description='Đường dẫn banner')
    news_category_id: str = Field(None, description='Loại tin')
    user_id: str = Field(..., description='user_id')
    user_name: Optional[str] = Field(None, description='Tên người tạo')
    content: str = Field(None, description="Nội dung")
    summary: str = Field(None, description="Tóm tắt nội dung")
    start_date: str = Field(None, description="Ngày bắt đầu")
    expired_date: str = Field(None, description="Ngày kết thúc")
    active_flag: str = Field(None, description="Trạng thái kích hoạt")


class NewsImageRequest(BaseSchema):
    @staticmethod
    def get_upload_request(
            avatar_image: UploadFile = File(...),
            thumbnail_image: UploadFile = File(...),
    ):
        return avatar_image, thumbnail_image
