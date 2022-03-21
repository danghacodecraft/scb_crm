from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse

########################################################################################################################
# Request
########################################################################################################################


class CategoryDropdownRequest(DropdownRequest):
    select_flag: bool = Field(False, description='`False`: Có. `True`: Không')


class DocumentsRequest(BaseSchema):
    id: str = Field(..., description='Id của loại tài liệu')
    url: str = Field(..., description='Đường dẫn biểu mẫu')
    # version: str = Field(..., description='Phiên bản biểu mẫu') #TODO: gọi DMS
    # name: str = Field(..., description='Tên biểu mẫu') #TODO: gọi DMS
    # active_flag: bool = Field(..., description='Trạng thái hoạt động') #TODO: gọi DMS
    # content_type: str = Field(..., description='Loại biểu mẫu') # TODO: chưa có chỗ lưu
    # size: str = Field(..., description='Kích thước biểu mẫu') # TODO: chưa có chỗ lưu
    # folder_name: str = Field(..., description='Thư mục biểu mẫu') # TODO: chưa có chỗ lưu
    # note: str = Field(..., description='Mô tả biểu mẫu') # TODO: chưa có chỗ lưu


class DocumentsListRequest(BaseSchema):
    language_type: DropdownRequest = Field(..., description='Ngôn ngữ biểu mẫu')
    documents: List[DocumentsRequest] = Field(..., description='Thông tin biểu mẫu `FATCA`')


class FatcaRequest(BaseSchema):
    fatca_information: List[CategoryDropdownRequest] = Field(..., description='Danh mục `FATCA`')
    # document_information: List[DocumentsListRequest] = Field(..., description='Danh sách biểu mẫu `FATCA`')


########################################################################################################################
# Response
########################################################################################################################

class CategoryDropdownResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh` loại Fatca')
    code: str = Field(..., description='`Mã` loại Fatca')
    name: str = Field(..., description='`Tên` loại Fatca')
    select_flag: bool = Field(False, description='`False`: Có. `True`: Không của loại Fatca')


class DocumentDependFatcaCategoryResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh` loại Fatca')
    code: str = Field(..., description='`Mã` loại Fatca')
    name: str = Field(..., description='`Tên` loại Fatca')
    url: str = Field(..., description='Đường dẫn biểu mẫu')
    # active_flag: bool = Field(..., description='Trạng thái biểu mẫu')
    version: str = Field(..., description='Phiên bản biểu mẫu')
    content_type: str = Field(..., description='Loại biểu mẫu')
    size: str = Field(..., description='Kích thước biểu mẫu')
    # folder_name: str = Field(..., description='Thư mục biểu mẫu')
    created_by: str = Field(..., description='Người tạo biểu mẫu')
    created_at: datetime = Field(..., description='Tạo mới vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')
    updated_by: str = Field(..., description='Người cập nhật biểu mẫu')
    updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')
    # note: str = Field(..., description='Mô tả biểu mẫu')


class DocumentsListResponse(BaseSchema):
    language_type: DropdownResponse = Field(..., description='Ngôn ngữ biểu mẫu')
    documents: List[DocumentDependFatcaCategoryResponse] = Field(..., description='Các tài liệu theo ngôn ngữ biểu mẫu')


class FatcaResponse(BaseSchema):
    fatca_information: List[CategoryDropdownResponse] = Field(..., description='Danh mục `FATCA`')
    document_information: List[DocumentsListResponse] = Field(..., description='Danh sách biểu mẫu `FATCA`')
