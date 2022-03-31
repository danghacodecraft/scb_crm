from datetime import datetime
from typing import List

from fastapi import Depends, File, Form, UploadFile
from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.schemas.utils import DropdownResponse


class NewsResponse(BaseSchema):
    news_id: str = Field(None, description='id tin tức')


class NewsDetailResponse(BaseSchema):
    id: str = Field(..., description='ID tin tức')
    title: str = Field(..., description='Tiêu đề')
    avatar_url: str = Field(None, description='avatar_url')
    thumbnail_url: str = Field(..., description='thumbnail_url')
    news_category_id: DropdownResponse = Field(..., description='Loại tin')
    user_name: str = Field(..., description='Tên người tạo')
    content: str = Field(None, description="Nội dung")
    summary: str = Field(None, description="Tóm tắt nội dung")
    start_date: datetime = Field(..., description="Ngày bắt đầu")
    expired_date: datetime = Field(None, description="Ngày kết thúc")
    created_at: datetime = Field(None, description="Ngày tạo tin")
    active_flag: int = Field(..., description="Trạng thái kích hoạt")


class ListNewsResponse(BaseSchema):
    num_news: int = Field(..., description='Tổng số tinh tức')
    list_news: List[NewsDetailResponse] = Field(None, description='Danh sách tinh tức')


class NewsImageRequest(BaseSchema):
    @staticmethod
    def get_upload_request(
            avatar_image: UploadFile = File(None),
            thumbnail_image: UploadFile = File(...),
            current_user=Depends(get_current_user_from_header()),
            title: str = Form(..., description='Tiêu đề'),
            news_category_id: str = Form(..., description='Loại tin'),
            content: str = Form(..., description="Nội dung"),
            summary: str = Form(..., description="Tóm tắt nội dung"),
            start_date: str = Form(..., description="Ngày bắt đầu"),
            expired_date: str = Form(None, description="Ngày kết thúc"),
            active_flag: int = Form(..., description="Trạng thái kích hoạt")
    ):
        return (avatar_image, thumbnail_image, current_user, title, news_category_id, content,
                summary, start_date, expired_date, active_flag)
