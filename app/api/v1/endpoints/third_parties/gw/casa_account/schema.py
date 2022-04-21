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


class GWAccountInfoResponse(BaseSchema):
    number: str = Field(..., description="Số tài khoản")
    type: str = Field(..., description="Loại tài khoản")
    type_name: str = Field(..., description="Tên loại tài khoản")
    currency: str = Field(..., description="Loại tiền trong tài khoản")
    balance: str = Field(..., description="Số dư tài khoản")
    balance_available: str = Field(..., description="Số dư có thể sử dụng")
    balance_lock: str = Field(..., description="Số dư bị phong tỏa")
    over_draft_limit: str = Field(..., description="Hạn mức thấu chi")
    over_draft_expired_date: str = Field(..., description="Ngày hết hạn")
    latest_transaction_date: str = Field(..., description="Ngày giao dịch gần nhất")
    open_date: str = Field(..., description="Ngày mở tài khoản")
    maturity_date: str = Field(..., description="Ngày đến hạn")
    status: str = Field(..., description="Tình trạng tài khoản (đóng, mở)")
    lock_status: str = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    class_name: str = Field(..., description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: str = Field(..., description="Mã sản phẩm")
    saving_serials: str = Field(..., description="Số Series Sổ tiết kiệm")
    pre_open_date: str = Field(..., description="Ngày cấp lại sổ")
    service: str = Field(..., description="Gói dịch vụ")
    service_date: str = Field(..., description="Ngày tham gia gói dịch vụ")
    company_salary: str = Field(..., description="Công ty chi lương")
    company_salary_num: str = Field(..., description="STK Công ty chi lương")
    service_escrow: str = Field(..., description="Dịch vụ ký quỹ")
    service_escrow_ex_date: str = Field(..., description="Ngày đáo hạn ký quỹ")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin đơn vị")


class GWCasaAccountResponse(BaseSchema):
    account_info: GWAccountInfoResponse = Field(..., description="Thông tin tài khoản")


class GWCasaAccountCheckExistResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCasaAccountCheckExistRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
