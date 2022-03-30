from typing import Optional

from fastapi import Depends, File, Form, UploadFile
from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.dependencies.authenticate import get_current_user_from_header


class NewsRequest(BaseSchema):
    tilte: str = Field(..., description='Tiêu đề')
    news_category_id: str = Field(..., description='Loại tin')
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
    user_name: Optional[str] = Field(None, description='Tên người tạo')
    content: str = Field(None, description="Nội dung")
    summary: str = Field(None, description="Tóm tắt nội dung")
    start_date: str = Field(None, description="Ngày bắt đầu")
    expired_date: str = Field(None, description="Ngày kết thúc")
    active_flag: str = Field(None, description="Trạng thái kích hoạt")


class NewsImageRequest(BaseSchema):
    @staticmethod
    def get_upload_request(
            avatar_image: UploadFile = File(None),
            thumbnail_image: UploadFile = File(None),
            current_user=Depends(get_current_user_from_header()),
            tilte: str = Form(None, description='Tiêu đề'),
            news_category_id: str = Form(None, description='Loại tin'),
            content: str = Form(None, description="Nội dung"),
            summary: str = Form(None, description="Tóm tắt nội dung"),
            start_date: str = Form(None, description="Ngày bắt đầu"),
            expired_date: str = Form(None, description="Ngày kết thúc"),
            active_flag: str = Form(None, description="Trạng thái kích hoạt")


    ):
        return (avatar_image, thumbnail_image, current_user, tilte, news_category_id, content,
                summary, start_date, expired_date, active_flag)
