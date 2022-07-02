from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import OptionalDropdownRequest


class ReceiverResponse(BaseSchema):
    withdraw_account_flag: bool = Field(..., description="`true`: Rút tài khoản"
                                                         "`false`: Rút cheque")
    currency: str = Field(..., description="Loại tiền")
    withdrawals_amount: int = Field(..., description="Số tiền")
    content: str = Field(..., description="Nội dung rút tiền")


class FeeInfoResponse(BaseSchema):
    is_transfer_payer: bool = Field(..., description="`true`: Có thu phí cùng giao dịch, Bên thanh toán phí: Bên chuyển"
                                                     "`false`: Có thu phí cùng giao dịch, Bên thanh toán phí: Bên nhận"
                                                     "`null`: Không thu phí cùng giao dịch")
    payer: Optional[str] = Field(..., description="Bên thanh toán phí")
    fee_amount: Optional[int] = Field(..., description="Số tiền phí")
    vat_tax: Optional[float] = Field(..., description="Thuế VAT")
    total: Optional[float] = Field(..., description="Tổng số tiền phí")
    actual_total: Optional[float] = Field(..., description="Số tiền thực chuyển")
    note: Optional[str] = Field(..., description="Ghi chú")


# Giao dịch rút tiền
class WithdrawResponse(BaseSchema):
    receiver_response: ReceiverResponse = Field(..., description="Thông tin người hưởng thụ")
    fee_response: FeeInfoResponse = Field(..., description="Thông tin phí")


class CasaAccountsResponse(BaseSchema):
    number: str = Field(..., description="Tài khoản thanh toán")
    fullname_vn: str = Field(..., description="Tên chủ tài khoản")
    balance_available: int = Field(..., description="Số dư khả dụng")
    currency: str = Field(..., description="Loại tiền")
    account_type: str = Field(..., description="Loại tài khoản")


# Danh sách tài khoản nguồn
class SourceAccountInfoResponse(BaseSchema):
    casa_accounts: List[CasaAccountsResponse] = Field(..., description="Tài khoản nguồn")
    total_items: int = Field(..., description="Tổng số tài khoản")


########################################################################################################################
# Request
########################################################################################################################
# I.Tài khoản  nguồn
class SourceAccountRequest(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản")


# II. Thông tin người hưởng thụ
class BeneficiaryInformationRequest(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    withdrawals_amount: int = Field(..., description="2. Số tiền")
    seri_cheque: OptionalDropdownRequest = Field(None, description="3. Seri Cheque")
    date_of_issue: Optional[date] = Field(None, description="4. Ngày ký phát")
    exchange_VND_flag: Optional[int] = Field(None, description='5. Quy đổi VND')
    exchange_rate: Optional[int] = Field(None, description="6. Tỉ giá")
    exchanged_money_VND: Optional[int] = Field(None, description="7. Số tiền quy đổi VND")
    reciprocal_rate_headquarters: Optional[int] = Field(None, description="8. Tỷ giá đối ứng hội sở")
    content: str = Field(..., description="9. Nội dung rút tiền")


# III. Thông tin phí
class FeeInformationRequest(BaseSchema):
    is_transfer_payer: bool = Field(
        ...,
        description=' 1. Cờ có thu phí hay không, `true`: Có thu phí, `false` = Không thu phí'
    )
    payer: Optional[str] = Field(..., description="Bên thanh toán phí")
    fee_amount: Optional[int] = Field(..., description="3. Số tiền phí")


# A. THÔNG TIN GIAO DỊCH
class TransactionInformationRequest(BaseSchema):
    source_accounts: SourceAccountRequest = Field(..., description="I. Tài khoản nguồn")
    beneficiary_information: BeneficiaryInformationRequest = Field(..., description="II. Thông tin người hưởng thụ")
    fee_information: Optional[FeeInformationRequest] = Field(None, description="III. Thông tin phí")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class TransactionalCustomerInformationRequest(BaseSchema):
    cif_number: str = CustomField(description="1. Mã khách hàng giao dịch").CIFNumberField
    note: str = Field(..., description="8. Ghi chú")


# Giao dịch rút tiền
class WithdrawRequest(BaseSchema):
    transaction_information: TransactionInformationRequest = Field(..., description="A. Thông tin giao dịch")
