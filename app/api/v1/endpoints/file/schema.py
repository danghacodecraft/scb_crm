from datetime import datetime
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class FileServiceResponse(BaseSchema):
    document_file_id: Optional[str] = Field(..., description='ID File tài liệu của CRM')
    created_at: datetime = Field(..., description='Tạo mới vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')
    created_by: str = Field(..., description='Tạo mới bởi')
    uuid: str = Field(..., description='Chuỗi định danh file trên service file')
    uuid_ekyc: str = Field(None, description="uuid call ekyc")
    file_url: str = Field(..., description='Link download file')
    name: str = Field(..., description='Tên file')
    content_type: str = Field(..., description='Content-Type của file')
    size: int = Field(..., description='Kích thước file')


class FileServiceDownloadFileResponse(BaseSchema):
    uuid: str = Field(..., description='Chuỗi định danh file trên service file')
    file_url: str = Field(..., description='Link download file')
    file_name: str = Field(..., description='Tên file')


class FileUploadResponse(BaseSchema):
    uuid: str = Field(..., description='Chuỗi định danh file trên service file')
    file_url: str = Field(..., description='Link download file')
    name: str = Field(..., description='Tên file')
    content_type: str = Field(..., description='Content-Type của file')
    size: int = Field(..., description='Kích thước file')
