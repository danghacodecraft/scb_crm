from datetime import datetime

from pydantic import Field

from app.api.base.schema import BaseSchema


class GWHistoryChangeFieldAccount(BaseSchema):
    maker: str = Field(..., description="Giao dịch viên")
    maker_time_stamp: datetime = Field(..., description="Ngày giờ Giao dịch viên thực hiện")
    checker: str = Field(..., description="Kiểm soát viên")
    checker_time_stamp: datetime = Field(..., description="Ngày giờ Kiểm soát viên thực hiện")
    field_name: str = Field(..., description="Tên trường dữ liệu thay đổi")
    old_value: str = Field(..., description="Giá trị cũ")
    new_value: str = Field(..., description="Giá trị mới")
