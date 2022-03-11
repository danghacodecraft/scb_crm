from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


# I.Tài khoản  nguồn
class SourceAccountResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name: str = Field(..., description="Tên đầy đủ của người dùng ")
    card_type: DropdownResponse = Field(..., description='Loại thẻ')
    payment_account: int = Field(..., description="Tài khoản thanh toán")
    available_balances: int = Field(..., description="Số dư khả dụng")
    currency: DropdownResponse = Field(..., description="Loại tiền")


# II. Thông tin người hưởng thụ
class BeneficiaryInformation(BaseSchema):
    withdraw_account_flag: bool = Field(..., description='Rút tài khoản / Rút cheque')
    currency: DropdownResponse = Field(..., description="Loại tiền")
    number_money: int = Field(..., description="Số tiền")
    seri_cheque: DropdownResponse = Field(None, description="Seri Cheque")
    date_of_issue: date = Field(..., description="Ngày ký phát")
    exchange_VND_flag: bool = Field(..., description='Quy đổi VND')
    exchange_rate: int = Field(..., description="Tỷ giá")
    exchanged_money_VND: DropdownResponse = Field(..., description="Số tiền quy đổi VND")
    reciprocal_rate_headquarters: int = Field(..., description="Tỷ giá đối ứng hội sở")
    withdrawal_content: str = Field(..., description="Nội dung rút tiền")
    journal_entry_number: str = Field(..., description="Số bút toán")


# III. Thông tin phí
class FeeInformation(BaseSchema):
    fees_same_transaction_flag: DropdownResponse = Field(..., description='Thu phí cùng giao dịch')
    fee_payer: DropdownResponse = Field(..., description="Bên thanh toán phí")
    fee_amount: int = Field(..., description="Số tiền phí")
    tax_VAT: int = Field(..., description="Số tiền thuế VAT")
    total_fee_amount: int = Field(..., description="Tổng số tiền phí")
    actual_amount_transferred: int = Field(..., description="Số tiền chuyển thực")
    note: str = Field(..., description="Ghi chú")


# A. THÔNG TIN GIAO DỊCH
class TransactionInformationResponse(BaseSchema):
    total_account: int = Field(..., description="Tổng số tài khoản")
    source_accounts: List[SourceAccountResponse] = Field(..., description="Tài khoản nguồn")
    beneficiary_information: BeneficiaryInformation = Field(..., description="Thông tin người hưởng thụ")
    fee_information: FeeInformation = Field(..., description="Thông tin phí")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class TransactionalCustomerInformationResponse(BaseSchema):
    CIF_flag: bool = Field(..., description='Có CIF/ Chưa có CIF')
    customer_code: str = Field(..., description="Mã khách hàng giao dịch")
    trades: str = Field(..., description="Người giao dịch")
    identity_document: str = Field(..., description="Giấy tờ định danh")
    issued_date: str = Field(..., description="Ngày cấp")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    address: str = Field(..., description="Địa chỉ")
    mobile_number: str = Field(..., description="Điện thoại")
    note: str = Field(..., description="Ghi chú")


# Giao dịch rút tiền
class WithdrawResponse(BaseSchema):
    transaction_code: DropdownResponse = Field(..., description="Mã giao dịch")
    transaction_information: TransactionInformationResponse = Field(..., description="Thông tin giao dịch")
    transactional_customer_information: TransactionalCustomerInformationResponse = Field(
        ...,
        description="Thông tin khách hàng giao dịch"
    )


########################################################################################################################
# Request
########################################################################################################################
class SourceAccountRequest(SourceAccountResponse):
    card_type: DropdownRequest = Field(..., description='Loại thẻ')
    currency: DropdownRequest = Field(..., description="Loại tiền")


class TransactionInformationRequest(BaseSchema):
    source_account: List[SourceAccountRequest] = Field(..., description="Tài khoản nguồn")
    beneficiary_information: BeneficiaryInformation = Field(..., description="Thông tin người hưởng thụ")
    fee_information: FeeInformation = Field(..., description="Thông tin phí")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class TransactionalCustomerInformationRequest(TransactionalCustomerInformationResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


# Giao dịch rút tiền
class SaveWithdrawRequest(BaseSchema):
    transaction_code: DropdownRequest = Field(..., description="Mã giao dịch")
    transaction_information: TransactionInformationRequest = Field(..., description="Thông tin giao dịch")
    transactional_customer_information: TransactionalCustomerInformationRequest = Field(
        ...,
        description="Thông tin khách hàng giao dịch"
    )
