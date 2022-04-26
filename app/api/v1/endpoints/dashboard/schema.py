from typing import Optional

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
