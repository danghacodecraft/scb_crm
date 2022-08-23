from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    SavePaymentAccountRequest
)
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse


class CasaOpenCasaRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    casa_accounts: List[SavePaymentAccountRequest] = Field(..., description="Danh sách TKTT")


class CasaAccountInfoResponse(BaseSchema):
    self_selected_account_flag: bool = Field(..., description="""Cờ tự chọn số tài khoản
                                                                  \nSố tài khoản thường => `False`
                                                                  \nSố tài khoản yêu cầu => `True`""")
    currency: DropdownResponse = Field(..., description="Loại tiền")
    account_type: DropdownResponse = Field(..., description="Gói tài khoản")
    account_class: DropdownResponse = Field(..., description="Loại hình tài khoản")
    account_structure_type_level_1: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 1")
    account_structure_type_level_2: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 2")
    account_structure_type_level_3: OptionalDropdownResponse = Field(..., description="Kiểu kiến trúc cấp 3")
    casa_account_number: Optional[str] = Field(..., description="Số tài khoản", nullable=True)
    account_salary_organization_account: Optional[str] = Field(..., description="Tài khoản của tổ chức chi lương",
                                                               nullable=True)
    account_salary_organization_name: Optional[str] = Field(..., description="Chủ tài khoản chi lương", nullable=True)
    approve_status: Optional[int] = Field(..., description="Trạng thái phê duyệt tài khoản", nullable=True)


class CasaAccountResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    account_info: CasaAccountInfoResponse = Field(..., description="Chi tiết tài khoản thanh toán")


class CasaOpenCasaResponse(BaseSchema):
    booking_parent_id: str = Field(..., description="Mã giao dịch")
    transaction_code: str = Field(..., description="Mã giao dịch")
    total_item: int = Field(..., description="Tổng số TKTT")
    casa_accounts: List[CasaAccountResponse] = Field(..., description="Danh sách TKTT")
