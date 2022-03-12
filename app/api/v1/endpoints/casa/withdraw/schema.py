from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownRequest
)


# I.Tài khoản  nguồn
class SourceAccountResponse(BaseSchema):
    user_id: str = Field(..., description="Id người dùng")
    full_name_vn: str = Field(..., description="Tên đầy đủ của người dùng")
    card_type: DropdownResponse = Field(..., description='Loại thẻ')
    payment_account: str = Field(..., description="1. Tài khoản thanh toán")
    available_balances: str = Field(..., description="2. Số dư khả dụng")


# II. Thông tin người hưởng thụ
class BeneficiaryInformationResponse(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    number_money: str = Field(..., description="2. Số tiền")
    seri_cheque: DropdownResponse = Field(None, description="3. Seri Cheque")
    date_of_issue: date = Field(..., description="4. Ngày ký phát")
    exchange_VND_flag: bool = Field(..., description='5. Quy đổi VND')
    exchange_rate: str = Field(..., description="6. Tỷ giá")
    exchanged_money_VND: str = Field(..., description="7. Số tiền quy đổi VND")
    reciprocal_rate_headquarters: str = Field(..., description="8. Tỷ giá đối ứng hội sở")
    withdrawal_content: str = Field(..., description="9. Nội dung rút tiền")
    journal_entry_number: str = Field(..., description="10. Số bút toán")


# III. Thông tin phí
class FeeInformationResponse(BaseSchema):
    fees_same_transaction_flag: DropdownResponse = Field(..., description='1. Thu phí cùng giao dịch')
    fee_payer: DropdownResponse = Field(..., description="2. Bên thanh toán phí")
    fee_amount: str = Field(..., description="3. Số tiền phí")
    tax_VAT: str = Field(..., description="4. Số tiền thuế VAT")
    total_fee_amount: str = Field(..., description="5. Tổng số tiền phí")
    actual_amount_transferred: str = Field(..., description="6. Số tiền thực chuyển")
    note: str = Field(..., description="7. Ghi chú")


# A. THÔNG TIN GIAO DỊCH
class TransactionInformationResponse(BaseSchema):
    currency: DropdownResponse = Field(..., description="Loại tiền")
    source_accounts: SourceAccountResponse = Field(..., description="I. Tài khoản nguồn")
    beneficiary_information: BeneficiaryInformationResponse = Field(..., description="II. Thông tin người hưởng thụ")
    fee_information: FeeInformationResponse = Field(..., description="III. Thông tin phí")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class TransactionalCustomerInformationResponse(BaseSchema):
    cif_flag: bool = Field(..., description='Có CIF/ Chưa có CIF')
    cif_number: str = CustomField(description="1. Mã khách hàng giao dịch").CIFNumberField
    trader: str = Field(..., description="2. Người giao dịch")
    identity_document: str = Field(..., description="3. Giấy tờ định danh")
    issued_date: date = Field(..., description="4. Ngày cấp")
    place_of_issue: DropdownResponse = Field(..., description="5. Nơi cấp")
    address: str = Field(..., description="6. Địa chỉ")
    mobile_number: str = Field(..., description="7. Điện thoại")
    note: str = Field(..., description="8. Ghi chú")


# Giao dịch rút tiền
class WithdrawResponse(BaseSchema):
    transaction_code: DropdownResponse = Field(..., description="Mã giao dịch")
    total_account: str = Field(..., description="Tổng số tài khoản")
    transaction_information: List[TransactionInformationResponse] = Field(..., description="A. Thông tin giao dịch")
    transactional_customer_information: TransactionalCustomerInformationResponse = Field(
        ...,
        description="B. Thông tin khách hàng giao dịch"
    )


########################################################################################################################
# Request
########################################################################################################################
# I.Tài khoản  nguồn
class SourceAccountRequest(BaseSchema):
    payment_account: str = Field(..., description="1. Tài khoản thanh toán")


# II. Thông tin người hưởng thụ
class BeneficiaryInformationRequest(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    number_money: str = Field(..., description="2. Số tiền")
    seri_cheque: OptionalDropdownRequest = Field(None, description="3. Seri Cheque")
    date_of_issue: Optional[date] = Field(None, description="4. Ngày ký phát")
    exchange_VND_flag: Optional[bool] = Field(None, description='5. Quy đổi VND')
    exchange_rate: Optional[str] = Field(None, description="6. Tỷ giá")
    exchanged_money_VND: Optional[str] = Field(None, description="7. Số tiền quy đổi VND")
    reciprocal_rate_headquarters: Optional[str] = Field(None, description="8. Tỷ giá đối ứng hội sở")
    withdrawal_content: str = Field(..., description="9. Nội dung rút tiền")


# III. Thông tin phí
class FeeInformationRequest(BaseSchema):
    fee_payer: DropdownRequest = Field(..., description="2. Bên thanh toán phí")
    fee_amount: str = Field(..., description="3. Số tiền phí")
    note: Optional[str] = Field(None, description="7. Ghi chú")


# A. THÔNG TIN GIAO DỊCH
class TransactionInformationRequest(BaseSchema):
    source_accounts: SourceAccountRequest = Field(..., description="I. Tài khoản nguồn")
    beneficiary_information: BeneficiaryInformationRequest = Field(..., description="II. Thông tin người hưởng thụ")
    fees_same_transaction_flag: DropdownRequest = Field(..., description='III -> 1. Thu phí cùng giao dịch')
    fee_information: Optional[FeeInformationRequest] = Field(None, description="III. Thông tin phí")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class TransactionalCustomerInformationRequest(BaseSchema):
    cif_number: str = CustomField(description="1. Mã khách hàng giao dịch").CIFNumberField
    note: str = Field(..., description="8. Ghi chú")


# Giao dịch rút tiền
class WithdrawRequest(BaseSchema):
    transaction_information: List[TransactionInformationRequest] = Field(..., description="A. Thông tin giao dịch")
    cif_flag: bool = Field(..., description='B -> 1. Có CIF/ Chưa có CIF')
    transactional_customer_information: Optional[TransactionalCustomerInformationRequest] = Field(
        None,
        description="B. Thông tin khách hàng giao dịch"
    )
