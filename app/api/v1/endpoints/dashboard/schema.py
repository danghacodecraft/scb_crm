from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class TransactionListResponse(BaseSchema):
    cif_id: str = Field(..., description="CIF ID")
    full_name_vn: str = Field(..., description="Tên khách hàng")
    booking_code: Optional[str] = Field(..., description="Mã booking")


class CustomerInfoResponse(BaseSchema):
    cif_id: str = Field(None, description="CIF id")
    cif_number: str = Field(None, description="CIF number")
    full_name: str = Field(None, description="Tên khách hàng")
    identity_number: str = Field(None, description="Giấy tờ định danh")
    phone_number: str = Field(None, description="Số điện thoại")
    street: str = Field(None, description="Số nhà - tên Đường")
    ward: DropdownResponse = Field(None, description="Phường - xã")
    district: DropdownResponse = Field(None, description="Quận - Huyện")
    province: DropdownResponse = Field(None, description="Tình thành")
    branch: DropdownResponse = Field(None, description="Chi nhánh")


class BranchResponse(BaseSchema):
    code: str = Field(..., description="Mã ")
    id: str = Field(..., description="CIF id")
    title: str = Field(..., description="Tiêu đề")
    unit: str = Field(..., description="Đơn vị")
    day: int = Field(..., description="Ngày")
    week: int = Field(..., description="Tuần")
    month: int = Field(..., description="Tháng")
    accumulated: int = Field(..., description="Tích lũy")
    amt_year: int = Field(..., description="amt năm")
    amt_ky_truoc: int = Field(..., description="amt kỳ trước")
    divisor_bal_lcl: int = Field(..., description="Divisor_bal_lcl")
    divider_bal_lcl: int = Field(..., description="Divider_bal_lcl")


class AccountingEntryResponse(BaseSchema):
    id: str = Field(..., description="Mã bút toán")
    title: str = Field(..., description="Tiêu đề bút toán")
    val: float = Field(..., description="Giá trị bút toán")
    unit: str = Field(..., description="Đơn vị bút toán")


class ListBranchesResponse(BaseSchema):
    branch_id: str = Field(..., description="Mã khu vực")
    branch_name: str = Field(..., description="Mã khu vực")
    longitude: float = Field(..., description="Kinh độ")
    latitude: float = Field(..., description="Vĩ độ")
    type: str = Field(..., description="Loại")


class AreaResponse(BaseSchema):
    ID: str = Field(..., description="Mã vùng")
    NAME: str = Field(..., description="Tên vùng")
    branches: List[ListBranchesResponse] = Field(..., description="Chi nhánh")
    left: float = Field(..., description="Left")
    right: float = Field(..., description="Right")
    top: float = Field(..., description="Top")
    bottom: float = Field(..., description="Bottom")
