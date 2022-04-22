from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.third_parties.gw.schema import (
    GWBranchDropdownResponse, GWCIFInfoResponse
)


class GWAccountInfoPayinAccResponse(BaseSchema):
    number: str = Field(..., description="""Số tài khoản nguồn
                                + Trường hợp p_payout_type='S' -->Truyền giá trị
                                + Trường hợp p_payout_type='Y' --> Null""")


class GWAccountInfoPayoutAccResponse(BaseSchema):
    number: str = Field(..., description="""Số tài khoản chỉ định lúc đáo hạn
                                + Trường hợp p_payout_type='S' -->Truyền giá trị
                                + Trường hợp p_payout_type='Y' --> Null""")


class GWAccountStaffInfoDirectResponse(BaseSchema):
    code: str = Field(..., description="Mã nhân viên")
    name: str = Field(..., description="Tên nhân viên")


class GWAccountStaffInfoIndirectResponse(BaseSchema):
    code: str = Field(..., description="Mã nhân viên")
    name: str = Field(..., description="Tên nhân viên")


class GWDepositAccountInfoResponse(BaseSchema):
    number: str = Field(..., description="Số tài khoản")
    term: str = Field(..., description="Kỳ hạn, 1 tháng ,2 tháng… Dành cho tài khoản tiết kiệm")
    type: str = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)"),
    type_name: str = Field(..., description="Tên loại tài khoản")
    saving_serials: str = Field(..., description="Số Series Sổ tiết kiệm")
    currency: str = Field(..., description="Loại tiền trong tài khoản")
    balance: str = Field(..., description="Số dư tài khoản")
    balance_available: str = Field(..., description="Số dư có thể sử dụng")
    open_date: str = Field(..., description="Ngày mở tài khoản")
    maturity_date: str = Field(..., description="Ngày đến hạn")
    lock_status: str = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    class_name: str = Field(..., description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: str = Field(..., description="Mã sản phẩm")
    interest_rate: str = Field(..., description="Lãi suất")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin chi nhánh")
    payin_account: GWAccountInfoPayinAccResponse = Field(..., description="Số tài khoản nguồn")
    payout_account: GWAccountInfoPayoutAccResponse = Field(..., description="Số tài khoản chỉ định lúc đáo hạn")
    staff_info_direct: GWAccountStaffInfoDirectResponse = Field(..., description="Thông tin nhân viên trực tiếp")
    staff_info_indirect: GWAccountStaffInfoIndirectResponse = Field(...,
                                                                    description="Thông tin nhân viên không trực tiếp")


class GWDepositCustomerInfoResponse(BaseSchema):
    fullname_vn: str = Field(..., description="Họ và tên")
    date_of_birth: str = Field(..., description="Ngày sinh")
    gender: str = Field(..., description="Giới tính")
    email: str = Field(..., description="Địa chỉ Email")
    mobile_phone: str = Field(..., description="Điện thoại di động")
    customer_type: str = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")


class GWDepositAccountTDResponse(BaseSchema):
    customer_info: GWDepositCustomerInfoResponse = Field(..., description="Thông tin người sỡ hữu tài khoản")
    cif_info: GWCIFInfoResponse = Field(..., description="Thông tin CIF")
    account_info: GWDepositAccountInfoResponse = Field(..., description="Thông tin tài khoản")


class GWDepositAccountByCIFNumberInfoResponse(BaseSchema):
    number: str = Field(..., description="Số tài khoản")
    term: str = Field(..., description="Kỳ hạn, 1 tháng ,2 tháng… Dành cho tài khoản tiết kiệm")
    type: str = Field(..., description="Loại tài khoản (thanh toán, tiết kiệm…)")
    type_name: str = Field(..., description="Tên loại tài khoản")
    currency: str = Field(..., description="Loại tiền trong tài khoản")
    balance: str = Field(..., description="Số dư tài khoản")
    balance_available: str = Field(..., description="Số dư có thể sử dụng")
    balance_lock: str = Field(..., description="Số dư bị phong tỏa")
    open_date: str = Field(..., description="Ngày mở tài khoản")
    maturity_date: str = Field(..., description="Ngày đến hạn")
    saving_serials: str = Field(..., description="Số Series Sổ tiết kiệm")
    class_name: str = Field(..., description="Tên sản phẩm. Ví dụ: Tiết kiệm thông thường, phát lộc phát tài…")
    class_code: str = Field(..., description="Mã sản phẩm")
    interest_rate: str = Field(..., description="Lãi suất")
    lock_status: str = Field(..., description="Trạng thái tài khoản (phong tỏa hoặc không)")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin chi nhánh")
    payin_account: GWAccountInfoPayinAccResponse = Field(..., description="Số tài khoản nguồn")
    payout_account: GWAccountInfoPayoutAccResponse = Field(..., description="Số tài khoản chỉ định lúc đáo hạn")


class GWDepositAccountByCIFNumberResponse(BaseSchema):
    total_balances: str = Field(..., description="Tổng số dư")
    total_items: int = Field(..., description="Số lượng tài khoản")
    account_info_list: List[GWDepositAccountByCIFNumberInfoResponse] = Field(
        ..., description="Thông tin danh sách tài khoản")
