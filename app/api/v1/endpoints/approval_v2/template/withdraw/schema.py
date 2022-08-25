from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import (
    BaseSchema, CreatedUpdatedBaseModel, ResponseRequestSchema,
    TMSResponseSchema
)
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownRequest


class FeeInfoResponse(BaseSchema):
    is_transfer_payer: bool = Field(..., description="Cờ thu phí cùng giao dịch, `true` = Có, `false` = Không")
    payer_flag: Optional[bool] = Field(None, description="Bên thanh toán phí, `true`: Bên chuyển, `false` = Bên nhận'")
    fee_amount: Optional[int] = Field(None, description="Số tiền phí")
    vat_tax: Optional[float] = Field(None, description="Thuế VAT")
    total: Optional[float] = Field(None, description="Tổng số tiền phí")
    actual_total: Optional[float] = Field(None, description="Số tiền thực chuyển")
    note: Optional[str] = Field(None, description="Ghi chú")

# class FeeInfoResponse(BaseSchema):
#     is_transfer_payer: bool = Field(
#         ...,
#         description=' 1. Cờ có thu phí hay không, `true`: Có thu phí, `false` = Không thu phí'
#     )
#     payer_flag: Optional[bool] = Field(None, description="Bên thanh toán phí, `true`: Bên chuyển, `false` = Bên nhận'")
#     amount: Optional[str] = Field(None, description="3. Số tiền phí")
#     note: Optional[str] = Field(None, description="Ghi chú")


class SourceAccountResponse(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản")


class ReceiverInfoResponse(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    currency: str = Field(..., description="1. Loại tiền")
    amount: str = Field(..., description="2. Số tiền")
    seri_cheque: OptionalDropdownRequest = Field(None, description="3. Seri Cheque")
    date_of_issue: Optional[date] = Field(None, description="4. Ngày ký phát")
    exchange_VND_flag: Optional[str] = Field(None, description='5. Quy đổi VND')
    exchange_rate: Optional[str] = Field(None, description="6. Tỉ giá")
    exchanged_money_VND: Optional[str] = Field(None, description="7. Số tiền quy đổi VND")
    reciprocal_rate_headquarters: Optional[str] = Field(None, description="8. Tỷ giá đối ứng hội sở")
    content: str = Field(..., description="9. Nội dung rút tiền")


class StatementsResponse(ResponseRequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: str = Field(..., description="Số lượng")
    into_money: str = Field('', description="Thành tiền")


class TransactionInfoResponse(BaseSchema):
    source_accounts: SourceAccountResponse = Field(..., description="I. Tài khoản nguồn")
    receiver_info: ReceiverInfoResponse = Field(..., description="II. Thông tin người hưởng thụ")
    fee_info: Optional[FeeInfoResponse] = Field(..., description="III. Thông tin phí")


class SenderInfoResponse(BaseSchema):
    # cif_flag: bool = Field(..., description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
    cif_number: Optional[str] = Field(None, description="Số CIF")
    fullname_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: Optional[DropdownResponse] = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_phone: Optional[str] = Field(None, description="SĐT")
    telephone: Optional[str] = Field(None, description="SĐT")
    otherphone: Optional[str] = Field(None, description="SĐT")
    note: Optional[str] = Field(None, description="Ghi chú")


class ManagementInfoResponse(BaseSchema):
    direct_staff_code: Optional[str] = Field(None, description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(None, description="Mã nhân viên quản lý gián tiếp")


class TMSStatementResponse(TMSResponseSchema):
    statements: List[StatementsResponse] = Field(..., description="Thông tin chi tiết bảng kê")
    total: str = Field(..., description="Tổng thành tiền")
    odd_difference: str = Field(..., description="Chênh lệch lẻ")
    total_number_of_bills: Optional[str] = Field('0', description="tổng số lượng bill")


class CustomerInfoResponse(BaseSchema):
    statement_info: TMSStatementResponse = Field(..., description="I.Thông tin bảng kê")
    management_info: ManagementInfoResponse = Field(..., description="II. Thông tin quản lý")
    sender_info: SenderInfoResponse = \
        Field(..., description="III. Thông tin khách hàng giao dịch")


class TMSWithdrawResponse(CreatedUpdatedBaseModel):
    transaction_info: TransactionInfoResponse = Field(..., description="A. Thông tin giao dịch")
    customer_info: CustomerInfoResponse = Field(..., description="B. Thông tin khách hàng giao dịch")
