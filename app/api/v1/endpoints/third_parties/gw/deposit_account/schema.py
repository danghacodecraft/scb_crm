from datetime import date
from typing import List, Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.third_parties.gw.schema import (
    GWBranchDropdownResponse, GWCIFInfoResponse
)


class GWDepositPayinAccountResponse(BaseSchema):
    number: Optional[str] = Field(..., description="""Số tài khoản nguồn
                                + Trường hợp p_payout_type='S' -->Truyền giá trị
                                + Trường hợp p_payout_type='Y' --> Null""")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWDepositPayoutAccountResponse(BaseSchema):
    number: Optional[str] = Field(..., description="""Số tài khoản chỉ định lúc đáo hạn
                                + Trường hợp p_payout_type='S' -->Truyền giá trị
                                + Trường hợp p_payout_type='Y' --> Null""")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWAccountStaffInfoDirectResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã nhân viên")
    name: Optional[str] = Field(..., description="Tên nhân viên")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWAccountStaffInfoIndirectResponse(BaseSchema):
    code: Optional[str] = Field(..., description="Mã nhân viên")
    name: Optional[str] = Field(..., description="Tên nhân viên")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWDepositAccountInfoResponse(BaseSchema):
    number: Optional[str] = Field(..., description="Số tài khoản")
    term: Optional[str] = Field(..., description="Kỳ hạn, 1 tháng ,2 tháng… Dành cho tài khoản tiết kiệm")
    type: Optional[str] = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: Optional[str] = Field(..., description="Tên loại tài khoản")
    saving_serials: Optional[str] = Field(..., description="Số Series Sổ tiết kiệm")
    currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    balance: Optional[int] = Field(..., description="Số dư tài khoản")
    balance_available: Optional[float] = Field(..., description="Số dư có thể sử dụng")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư tài khoản có thể sử dụng vnd")
    balance_lock: Optional[float] = Field(..., description="Số dư tài khoản bị phong tỏa")
    interest_receivable_type: Optional[str] = Field(..., description="Hình thức lĩnh lãi")
    open_date: Optional[date] = Field(..., description="Ngày mở tài khoản")
    maturity_date: Optional[date] = Field(..., description="Ngày đến hạn")
    lock_status: Optional[str] = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    class_name: Optional[str] = Field(...,
                                      description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: Optional[str] = Field(..., description="Mã sản phẩm")
    interest_rate: Optional[str] = Field(..., description="Lãi suất")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin chi nhánh")
    payin_account: GWDepositPayinAccountResponse = Field(..., description="Số tài khoản nguồn")
    payout_account: GWDepositPayoutAccountResponse = Field(..., description="Số tài khoản chỉ định lúc đáo hạn")
    staff_info_direct: GWAccountStaffInfoDirectResponse = Field(..., description="Thông tin nhân viên trực tiếp")
    staff_info_indirect: GWAccountStaffInfoIndirectResponse = Field(...,
                                                                    description="Thông tin nhân viên không trực tiếp")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWDepositCustomerInfoResponse(BaseSchema):
    fullname_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[str] = Field(..., description="Ngày sinh")
    gender: Optional[str] = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ Email")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    type: Optional[str] = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWDepositAccountTDResponse(BaseSchema):
    customer_info: GWDepositCustomerInfoResponse = Field(..., description="Thông tin người sỡ hữu tài khoản")
    cif_info: GWCIFInfoResponse = Field(..., description="Thông tin CIF")
    account_info: GWDepositAccountInfoResponse = Field(..., description="Thông tin tài khoản")


class GWDepositAccountByCIFNumberInfoResponse(BaseSchema):
    number: Optional[str] = Field(..., description="Số tài khoản")
    term: Optional[str] = Field(..., description="Kỳ hạn, 1 tháng ,2 tháng… Dành cho tài khoản tiết kiệm")
    type: Optional[str] = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: Optional[str] = Field(..., description="Tên loại tài khoản")
    currency: Optional[str] = Field(..., description="Loại tiền trong tài khoản")
    balance: Optional[int] = Field(..., description="Số dư tài khoản")
    balance_available: Optional[float] = Field(..., description="Số dư có thể sử dụng")
    balance_available_vnd: Optional[int] = Field(..., description="Số dư tài khoản có thể sử dụng vnd")
    balance_lock: Optional[str] = Field(..., description="Số dư bị phong tỏa")
    open_date: Optional[date] = Field(..., description="Ngày mở tài khoản")
    maturity_date: Optional[date] = Field(..., description="Ngày đến hạn")
    saving_serials: Optional[str] = Field(..., description="Số Series Sổ tiết kiệm")
    class_name: Optional[str] = Field(...,
                                      description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: Optional[str] = Field(..., description="Mã sản phẩm")
    interest_rate: Optional[str] = Field(..., description="Lãi suất")
    lock_status: Optional[str] = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin chi nhánh")
    payin_account: GWDepositPayinAccountResponse = Field(..., description="Số tài khoản nguồn")
    payout_account: GWDepositPayoutAccountResponse = Field(..., description="Số tài khoản chỉ định lúc đáo hạn")

    @validator('*', pre=True)
    def check_blank_str(string):
        if string == '':
            return None
        return string


class GWDepositAccountByCIFNumberResponse(BaseSchema):
    total_balances: Optional[int] = Field(..., description="Tổng số dư")
    total_items: Optional[int] = Field(..., description="Số lượng tài khoản")
    account_info_list: List[GWDepositAccountByCIFNumberInfoResponse] = Field(
        ..., description="Thông tin danh sách tài khoản")
