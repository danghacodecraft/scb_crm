from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.third_parties.gw.casa_account.example import (
    CASA_ACCOUNT_NUMBER
)
from app.api.v1.endpoints.third_parties.gw.schema import (
    GWBranchDropdownResponse, GWCIFInfoResponse
)
from app.api.v1.schemas.utils import DropdownResponse


class CasaAccountByCIFNumberResponse(BaseSchema):
    number: Optional[str] = Field(..., description="Số tài khoản")
    type: Optional[str] = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: Optional[str] = Field(..., description="Tên loại tài khoản")
    currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    balance: Optional[int] = Field(..., description="Số dư tài khoản")
    balance_available: Optional[float] = Field(..., description="Số dư có thể sử dụng")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư tài khoản có thể sử dụng vnd")
    balance_lock: Optional[float] = Field(..., description="Số dư bị phong tỏa")
    over_draft_limit: Optional[str] = Field(..., description="Hạn mức thấu chi")
    over_draft_expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    latest_trans_date: Optional[date] = Field(..., description="Ngày giao dịch gần nhất")
    open_date: Optional[date] = Field(..., description="Ngày mở tài khoản")
    maturity_date: Optional[date] = Field(..., description="Ngày đến hạn")
    lock_status: Optional[str] = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    class_name: Optional[str] = Field(
        ...,
        description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…"
    )
    class_code: Optional[str] = Field(..., description="Mã sản phẩm")
    branch_info: GWBranchDropdownResponse = Field(...)


class GWCasaAccountByCIFNumberResponse(BaseSchema):
    total_balances: int = Field(..., description="Tổng số dư")
    total_items: int = Field(..., description="Số lượng tài khoản")
    account_info_list: List[CasaAccountByCIFNumberResponse] = Field(..., description="Chi tiết tài khoản")


class GWCasaAccountByCIFNumberRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerInfoResponse(BaseSchema):
    fullname_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[str] = Field(..., description="Ngày sinh")
    gender: Optional[str] = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Email")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    type: Optional[str] = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")


class GWAccountInfoResponse(BaseSchema):
    number: Optional[str] = Field(..., description="Số tài khoản")
    type: Optional[str] = Field(..., description="Loại tài khoản")
    type_name: Optional[str] = Field(..., description="Tên loại tài khoản")
    currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    balance: Optional[int] = Field(..., description="Số dư tài khoản")
    balance_available: Optional[float] = Field(..., description="Số dư có thể sử dụng")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư tài khoản có thể sử dụng vnd")
    balance_lock: Optional[float] = Field(..., description="Số dư bị phong tỏa")
    over_draft_limit: Optional[str] = Field(..., description="Hạn mức thấu chi")
    over_draft_expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    latest_transaction_date: Optional[date] = Field(..., description="Ngày giao dịch gần nhất")
    open_date: Optional[date] = Field(..., description="Ngày mở tài khoản")
    maturity_date: Optional[date] = Field(..., description="Ngày đến hạn")
    status: List[DropdownResponse] = Field(..., description="Trạng thái tài khoản (no debits, no credit..)")
    lock_status: Optional[str] = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    class_name: Optional[str] = Field(...,
                                      description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: Optional[str] = Field(..., description="Mã sản phẩm")
    saving_serials: Optional[str] = Field(..., description="Số Series Sổ tiết kiệm")
    pre_open_date: Optional[date] = Field(..., description="Ngày cấp lại sổ")
    service: Optional[str] = Field(..., description="Gói dịch vụ")
    service_date: Optional[date] = Field(..., description="Ngày tham gia gói dịch vụ")
    company_salary: Optional[str] = Field(..., description="Công ty chi lương")
    company_salary_num: Optional[str] = Field(..., description="STK Công ty chi lương")
    service_escrow: Optional[str] = Field(..., description="Dịch vụ ký quỹ")
    service_escrow_ex_date: Optional[date] = Field(..., description="Ngày đáo hạn ký quỹ")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin đơn vị")
    product_package: Optional[str] = Field(..., description="Gói sản phẩm")


class GWCasaAccountResponse(BaseSchema):
    customer_info: GWCustomerInfoResponse = Field(..., description="Thông tin người sỡ hữu tài khoản")
    cif_info: GWCIFInfoResponse = Field(..., description="Thông tin CIF")
    account_info: GWAccountInfoResponse = Field(..., description="Thông tin tài khoản")


class GWReportPieChartHistoryAccountInfoRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản", example=CASA_ACCOUNT_NUMBER)


class GWReportPieChartHistoryAccountInfoResponse(BaseSchema):
    transaction_type: str = Field(
        ..., description="""Loại giao dịch. VD: Chuyển tiền đi, Chi tiêu thẻ,
        Chuyển tiền đến, Rút tiền mặt, Nộp tiền mặt, Thanh toán hóa đơn, Khác"""
    )
    transaction_count: int = Field(..., description="Số lượng giao dịch")
    transaction_value: int = Field(..., description="Giá trị giao dịch")
    value_percent: float = Field(0, description="Phần trăm giá trị giao dịch")
    count_percent: float = Field(0, description="Phần trăm số lượng giao dịch")


class GWCasaAccountCheckExistResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCasaAccountCheckExistRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")


class GWReportColumnResponse(BaseSchema):
    transaction_type: str = Field(..., description="Loại giao dịch. VD: Rút, Gửi")
    transaction_value: int = Field(..., description="Giá trị giao dịch")


class GWReportColumnChart(BaseSchema):
    transaction_date: Optional[date] = Field(..., description="Ngày giao dịch")
    withdraw: Optional[GWReportColumnResponse] = Field(description="Giao dịch rút tiền")
    send: Optional[GWReportColumnResponse] = Field(description="Giao dịch gửi tiền")


class GWReportColumnChartHistoryAccountInfoResponse(BaseSchema):
    fullname_vn: str = Field(..., description="Họ và tên")
    type: str = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: str = Field(..., description="Tên loại tài khoản")
    number: str = Field(..., description="Số tài khoản")
    currency: str = Field(..., description="Loại tiền trong tài khoản")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư khả dụng trong tài khoản vnd")
    report_casa_account: List[GWReportColumnChart] = Field(..., escription="Báo cáo tài khoản CASA")


class GWReportColumnChartHistoryAccountInfoRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    from_date: date = Field(date(year=2020, month=4, day=20), description="Từ ngày")
    to_date: date = Field(date(year=2025, month=7, day=20), description="Đến ngày")


class GWReportStatementHistoryAccountInfoRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    from_date: date = Field(date(year=2020, month=4, day=20), description="Từ ngày")
    to_date: date = Field(date(year=2025, month=7, day=20), description="Đến ngày")


class GWReportStatementHistoryAccountInfoResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã giao dịch")
    transaction_date: Optional[date] = Field(..., description="Ngày giao dịch")
    description: Optional[str] = Field(..., description="Chi tiết giao dịch")
    channel: Optional[str] = Field(..., description="Kênh giao dịch")
    transaction_type: Optional[str] = Field(..., description="Hình thức giao dịch")
    credit: Optional[int] = Field(..., description="Ghi có")
    debit: Optional[int] = Field(..., description="Ghi nợ")
    balance: Optional[int] = Field(..., description="Số dư")
