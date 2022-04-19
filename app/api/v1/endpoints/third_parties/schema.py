from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField


class GWBranchDropdownResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị")
    branch_name: str = Field(..., description="Tên đơn vị không dấu")


class CasaAccountByCIFNumberResponse(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản")
    account_type: str = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    account_type_name: str = Field(..., description="Tên loại tài khoản")
    account_currency: str = Field(..., description="Loại tiền trong tài khoản")
    account_balance: str = Field(..., description="Số dư tài khoản")
    account_balance_available: str = Field(..., description="Số dư có thể sử dụng")
    account_balance_lock: str = Field(..., description="Số dư bị phong tỏa")
    account_over_draft_limit: str = Field(..., description="Hạn mức thấu chi")
    account_over_draft_expired_date: str = Field(..., description="Ngày hết hạn")
    account_latest_trans_date: str = Field(..., description="Ngày giao dịch gần nhất")
    account_open_date: str = Field(..., description="Ngày mở tài khoản")
    account_maturity_date: str = Field(..., description="Ngày đến hạn")
    account_lock_status: str = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    account_class_name: str = Field(
        ...,
        description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…"
    )
    account_class_code: Optional[str] = Field(..., description="Mã sản phẩm")
    branch_info: GWBranchDropdownResponse = Field(...)


class GWCasaAccountByCIFNumberResponse(BaseSchema):
    account_info_list: List[CasaAccountByCIFNumberResponse] = Field(..., description="Chi tiết tài khoản")
    total_balances: str = Field(..., description="Tổng số dư")
    total_items: int = Field(..., description="Số lượng tài khoản")


class GWCasaAccountByCIFNumberRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
