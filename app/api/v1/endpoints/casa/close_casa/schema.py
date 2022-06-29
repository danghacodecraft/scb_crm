from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, OptionalDropdownRequest


class AccountListRequest(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản")
    content: str = Field(..., description="Content")
    cheque_refundable: List[int] = Field(..., description="Séc nộp lại")


class OriginalCurrencyRequest(BaseSchema):
    receipt_type: str = Field(..., description="""
        `CASH`: Tài khoản treo tiền gửi đơn vị
        `CASA`: Chuyển khoản
    """)
    amount_money: int = Field(..., description="Số tiền")
    content: str = Field(..., description="Content")
    account_no: Optional[str] = Field(..., description="Số tài khoản")
    type: OptionalDropdownRequest = Field(..., description="Loại")
    form_of_receipt: OptionalDropdownRequest = Field(..., description="Hình thức nhận")


class SellForeignCurrencyRequest(BaseSchema):
    amount_money: int = Field(..., description="Số tiền")
    buying_rate: int = Field(..., description="Tỷ giá mua")
    reciprocal_rate: int = Field(..., description="Tỷ giá đối ứng HO")
    content: str = Field(..., description="Content")
    form_of_receipt: DropdownRequest = Field(..., description="Hình thức nhận")


class AdditionalFeeResquest(BaseSchema):
    fee_group: DropdownRequest = Field(..., description="Nhóm phí")
    fee_type: DropdownRequest = Field(..., description="Loại phí")
    amount_money: int = Field(..., description="Số tiền")
    content: str = Field(..., description="Diễn giải")


class FeeInfoRequest(BaseSchema):
    flag_fee_info: int = Field(..., description="""
        1: Trừ trong số tiền nhận
        2: Tiền mặt
        3: Tài khoản thanh toán
    """)
    account_num: str = Field(..., description="Số tài khoản")
    additional_fee: List[AdditionalFeeResquest] = Field(..., description="Thêm phí")


class SourceOfMoneyRequest(BaseSchema):
    flag_original_currency: bool = Field(..., description="Cờ nhận nguyên tệ")
    original_currency: OriginalCurrencyRequest = Field(..., description="Nhận nguyên tệ")
    flag_sell_foreign_currency: bool = Field(..., description="Cờ bán ngoại tệ cho SCB")
    sell_foreign_currency_to_SCB: Optional[SellForeignCurrencyRequest] = Field(..., description="Bán ngoại tệ")


class ManagementInfoRequest(BaseSchema):
    indirect_management_employee_code: str = Field(..., description="Mã nhân viên quản lý gián tiếp")
    sales_staff_code: str = Field(..., description="Mã nhân viên kinh doanh")


class CustomerInfoRequest(BaseSchema):
    customer_code: str = Field(..., description="Mã khách hàng giao dịch")


class TransactionalCustomerInfoRequest(BaseSchema):
    management_info: ManagementInfoRequest = Field(..., description="IV.1. Thông tin quản lý ")
    transactional_customer_info: CustomerInfoRequest = \
        Field(..., description="IV.2. Thông tin khách hàng giao dịch")


class ContentRequest(BaseSchema):
    note: str = Field(..., description="Ghi chú")


class TransactionFeePaymentInfoRequest(BaseSchema):
    source_of_money: SourceOfMoneyRequest = Field(..., description="I. Nguồn nhận tiền")
    # fee_info: FeeInfoRequest = Field(..., description="II. Thông tin phí")
    # transactional_customer_info: TransactionalCustomerInfoRequest = \
    #     Field(..., description="IV. Thông tin khách hàng giao dịch")
    # content: ContentRequest = Field(..., description="V. Ghi chú")


class CloseCasaRequest(BaseSchema):
    account_list: List[AccountListRequest] = Field(..., description="A. Danh sách tài khoản")
    transaction_fee_payment_info: TransactionFeePaymentInfoRequest = \
        Field(..., description="B. Thông tin thanh toán phí giao dịch")
