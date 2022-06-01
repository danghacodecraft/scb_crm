from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseGWSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.third_parties.gw.casa_account.example import (
    CASA_ACCOUNT_NUMBER
)
from app.api.v1.endpoints.third_parties.gw.schema import (
    GWBranchDropdownResponse, GWCIFInfoResponse
)
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse


class CasaAccountByCIFNumberResponse(BaseGWSchema):
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


class GWCasaAccountByCIFNumberResponse(BaseGWSchema):
    total_balances: int = Field(..., description="Tổng số dư")
    total_items: int = Field(..., description="Số lượng tài khoản")
    account_info_list: List[CasaAccountByCIFNumberResponse] = Field(..., description="Chi tiết tài khoản")


class GWCasaAccountByCIFNumberRequest(BaseGWSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerInfoResponse(BaseGWSchema):
    fullname_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[str] = Field(..., description="Ngày sinh")
    gender: Optional[str] = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Email")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    type: Optional[str] = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")


class GWCasaAccountLockInfo(BaseGWSchema):
    balance_lock: Optional[str] = Field(..., description="Số dư lock")
    date_lock: Optional[str] = Field(..., description="Ngày lock")
    expire_date_lock: Optional[str] = Field(..., description="Ngày hết hạn lock")
    type_code_lock: Optional[str] = Field(..., description="Mã loại lock")
    type_name_lock: Optional[str] = Field(..., description="Tên loại lock")
    reason_lock: Optional[str] = Field(..., description="Lý do lock")
    ref_no: Optional[str] = Field(..., description="Số ref")


class GWAccountInfoResponse(BaseGWSchema):
    number: Optional[str] = Field(..., description="Số tài khoản")
    type: Optional[str] = Field(..., description="Loại tài khoản")
    type_name: Optional[str] = Field(..., description="Tên loại tài khoản")
    currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    product_package: Optional[str] = Field(..., description="Gói sản phẩm")
    balance: Optional[int] = Field(..., description="Số dư tài khoản")
    balance_available: Optional[float] = Field(..., description="Số dư có thể sử dụng")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư tài khoản có thể sử dụng vnd")
    balance_lock: Optional[float] = Field(..., description="Số dư bị phong tỏa")
    over_draft_limit: Optional[str] = Field(..., description="Hạn mức thấu chi")
    over_draft_used: Optional[str] = Field(..., description="Hạn mức thấu chi đã sử dụng")
    over_draft_remain: Optional[str] = Field(..., description="Hạn mức thấu chi còn lại")
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
    lock_info: List[GWCasaAccountLockInfo] = Field(..., description="Thông tin tài khoản")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin đơn vị")
    staff_info_direct: OptionalDropdownResponse = Field(..., description="Thông tin nhân viên trực tiếp")
    staff_info_indirect: OptionalDropdownResponse = Field(..., description="Thông tin nhân viên không trực tiếp")


class GWCasaAccountResponse(BaseGWSchema):
    customer_info: GWCustomerInfoResponse = Field(..., description="Thông tin người sỡ hữu tài khoản")
    cif_info: GWCIFInfoResponse = Field(..., description="Thông tin CIF")
    account_info: GWAccountInfoResponse = Field(..., description="Thông tin tài khoản")


class GWReportPieChartHistoryAccountInfoRequest(BaseGWSchema):
    account_number: str = Field(..., description="Số tài khoản", example=CASA_ACCOUNT_NUMBER)


class GWReportPieChartHistoryAccountInfoResponse(BaseGWSchema):
    transaction_type: str = Field(
        ..., description="""Loại giao dịch. VD: Chuyển tiền đi, Chi tiêu thẻ,
        Chuyển tiền đến, Rút tiền mặt, Nộp tiền mặt, Thanh toán hóa đơn, Khác"""
    )
    transaction_count: int = Field(..., description="Số lượng giao dịch")
    transaction_value: int = Field(..., description="Giá trị giao dịch")
    value_percent: float = Field(0, description="Phần trăm giá trị giao dịch")
    count_percent: float = Field(0, description="Phần trăm số lượng giao dịch")


class GWCasaAccountCheckExistResponse(BaseGWSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCasaAccountCheckExistRequest(BaseGWSchema):
    account_number: str = Field(..., description="Số tài khoản")


class GWReportColumnResponse(BaseGWSchema):
    transaction_type: str = Field(..., description="Loại giao dịch. VD: Rút, Gửi")
    transaction_value: int = Field(..., description="Giá trị giao dịch")


class GWReportColumnChart(BaseGWSchema):
    transaction_date: Optional[date] = Field(..., description="Ngày giao dịch")
    withdraw: Optional[GWReportColumnResponse] = Field(description="Giao dịch rút tiền")
    send: Optional[GWReportColumnResponse] = Field(description="Giao dịch gửi tiền")


class GWReportColumnChartHistoryAccountInfoResponse(BaseGWSchema):
    fullname_vn: str = Field(..., description="Họ và tên")
    type: str = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: str = Field(..., description="Tên loại tài khoản")
    number: str = Field(..., description="Số tài khoản")
    currency: str = Field(..., description="Loại tiền trong tài khoản")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư khả dụng trong tài khoản vnd")
    report_casa_account: List[GWReportColumnChart] = Field(..., escription="Báo cáo tài khoản CASA")


class GWReportColumnChartHistoryAccountInfoRequest(BaseGWSchema):
    account_number: str = Field(..., description="Số tài khoản")
    from_date: date = Field(date(year=2020, month=4, day=20), description="Từ ngày")
    to_date: date = Field(date(year=2025, month=7, day=20), description="Đến ngày")


class GWReportStatementHistoryAccountInfoRequest(BaseGWSchema):
    account_number: str = Field(..., description="Số tài khoản")
    from_date: date = Field(date(year=2020, month=4, day=20), description="Từ ngày")
    to_date: date = Field(date(year=2025, month=7, day=20), description="Đến ngày")


class GWReportStatementHistoryAccountInfoResponse(BaseGWSchema):
    code: Optional[str] = Field(..., description="Mã giao dịch")
    transaction_date: Optional[date] = Field(..., description="Ngày giao dịch")
    description: Optional[str] = Field(..., description="Chi tiết giao dịch")
    channel: Optional[str] = Field(..., description="Kênh giao dịch")
    transaction_type: Optional[str] = Field(..., description="Hình thức giao dịch")
    credit: Optional[int] = Field(..., description="Ghi có")
    debit: Optional[int] = Field(..., description="Ghi nợ")
    balance: Optional[int] = Field(..., description="Số dư")


class GWReportStatementHistoryTDAccountInfoResponse(BaseGWSchema):
    code: Optional[str] = Field(..., description="Mã giao dịch")
    transaction_date: Optional[date] = Field(..., description="Ngày giao dịch")
    description: Optional[str] = Field(..., description="Chi tiết giao dịch")
    amount: Optional[str] = Field(..., description="Số tiền")
    rate: Optional[str] = Field(..., description="Lãi suất")
    balance: Optional[int] = Field(..., description="Số dư cuối giao dịch")
    expire_date: Optional[date] = Field(..., description='Ngày đến hạn')


class GWCIFInfoOpenCasaRequest(BaseGWSchema):
    cif_num: Optional[str] = CustomField().OptionalCIFNumberField


class GWAccountInfoOpenCasaRequest(BaseGWSchema):
    acc_spl: Optional[str] = Field(..., description="Tùy chọn tài khoản số đẹp Y/N")
    account_num: Optional[str] = Field(..., description="Số tài khoản")
    account_currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    account_class_code: Optional[str] = Field(..., description="Mã sản phẩm")


class GWStaffInfoCheckerCasaRequest(BaseGWSchema):
    staff_name: str = Field(..., description="Tên nhân viên")


class GWStaffInfoMakerCasaRequest(BaseGWSchema):
    staff_name: str = Field(..., description="Tên nhân viên")


class GWUdfItemJsonArrayOpenCasaRequest(BaseGWSchema):
    UDF_NAME: Optional[str] = Field(..., description="Tên UDF")
    UDF_VALUE: Optional[str] = Field(..., description="Giá trị UDF")


class GWUdfInfoOpenCasaRequest(BaseGWSchema):
    udf_json_array: List[GWUdfItemJsonArrayOpenCasaRequest] = Field(..., description="Giá trị nhập thêm kiểu json arr")


class GWOpenCasaAccountRequest(BaseGWSchema):
    cif_info: GWCIFInfoOpenCasaRequest = Field(..., description="Thông tin CIF")
    account_info: GWAccountInfoOpenCasaRequest = Field(..., description="Thông tin tài khoản")
    staff_info_checker: GWStaffInfoCheckerCasaRequest = Field(..., description="Thông tin nhân viên kiểm tra")
    staff_info_maker: GWStaffInfoMakerCasaRequest = Field(..., description="Thông tin nhân viên tạo tài khoản")
    udf_info: GWUdfInfoOpenCasaRequest = Field(..., description="Thông tin UDF")


class GWOpenCasaAccountResponse(BaseGWSchema):
    number: str = Field(..., description="Số tài khoản thanh toán")


class GWAccountInfoCloseCasaRequest(BaseGWSchema):
    account_num: Optional[str] = Field(..., description="Số tài khoản")


class GWCloseCasaClosureResponse(BaseGWSchema):
    close_mode: str = Field(..., description="CLOSE_MODE")
    account_no: str = Field(..., description="Số tài khoản")


class GWCloseCasaAccountRequest(BaseGWSchema):
    account_info: GWAccountInfoCloseCasaRequest = Field(..., description="Thông tin tài khoản")
    p_blk_closure: List[GWCloseCasaClosureResponse] = Field(..., description="Json Array CLOSE_MODE")
    p_blk_charge_main: Optional[str] = Field(..., description="P Blk Charge Main")
    p_blk_charge_details: Optional[str] = Field(..., description="P Blk Charge Details")
    p_blk_udf: Optional[str] = Field(..., description="P Blk Udf")
    staff_info_checker: GWStaffInfoCheckerCasaRequest = Field(..., description="Thông tin nhân viên kiểm tra")
    staff_info_maker: GWStaffInfoMakerCasaRequest = Field(..., description="Thông tin nhân viên đóng tài khoản")


class GWCloseCasaAccountResponse(BaseGWSchema):
    number: str = Field(..., description="Số tài khoản thanh toán")
