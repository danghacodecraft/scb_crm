from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.others.fee.schema import MultipleFeeInfoRequest


class TdAccountRequest(BaseSchema):
    currency_id: str = Field(..., description='Loại tiền')
    account_type_id: str = Field(..., description='Loại nhóm sản phẩm (gói) tài khoản')
    account_class_id: str = Field(..., description='Loại hình tài khoản')
    amount: Optional[int] = Field(None, description='Số dư hiện tại')
    pay_in_amount: int = Field(..., description='Thông tin nguồn tiền đầu vào')
    pay_out_interest_casa_account: str = Field(..., description='Tài khoản nhận lãi')
    pay_out_casa_account: str = Field(..., description='Tài khoản nhận gốc')
    td_contract_num: str = Field(..., description='Số hợp đồng')
    fcc_transaction_num: str = Field(None, description='Số bút toán (FCC)')
    maturity_date: date = Field(..., description='Ngày đáo hạn')
    td_serial: str = Field(..., description='Số serial')
    td_interest_type: str = Field(..., description='Hình thức lãi')
    td_interest: str = Field(..., description='Lãi suất tiết kiệm')
    td_rollover_type: Optional[str] = Field(...,
                                            description='Chỉ định khi đến hạn:I = Tái ký gốc + lãi ,P = Tái ký gốc')
    pay_out_casa_account_resign: Optional[str] = Field(..., description='Tài khoản nhận lãi tái ký')
    td_interest_class_resign: Optional[str] = Field(..., description='Hình thức lãi tái ký')
    acc_class_id_resign: Optional[str] = Field(..., description='Loại hình tài khoản tái ký')
    acc_type_id_resign: Optional[str] = Field(..., description='Loại nhóm sản phẩm (gói) tài khoản tái ký')


class DepositOpenTDAccountRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    td_account: List[TdAccountRequest] = Field(..., description="Danh sách TKTK")


class AccountForm(BaseSchema):
    pay_in: str = Field(..., description="Hình thức hạch toán")
    account_number: Optional[str] = Field(..., description="Số tài khoản")
    full_name: Optional[str] = Field(..., description="Chủ tài khoản")
    currency: Optional[str] = Field(..., description="Loại tiền")
    amount: Optional[str] = Field(..., description="Số dư khả dụng")


class CurrencyExchange(BaseSchema):
    currency_exchange: bool = Field(False, description="Quy đổi ngoại tệ")
    currency: Optional[str] = Field(..., description="Loại tiền")
    amount: Optional[str] = Field(..., description="Số tiền")
    rate: Optional[str] = Field(..., description="Tỷ giá(CCY/VND)")
    total: Optional[str] = Field(..., description="Thành tiền(VND)")
    description: Optional[str] = Field(..., description="Diễn giải")
    transaction_num: Optional[str] = Field(..., description="Số bút toán")


class CurrencyTransfer(BaseSchema):
    currency_transfer_flag: bool = Field(False)
    currency: Optional[str] = Field(..., description="Loại tiền")
    amount: Optional[str] = Field(..., description="Số tiền")


class PayInAccount(BaseSchema):
    pay_in_flag: bool = Field(False)
    amount: Optional[str] = Field(..., description="Số tiền")
    description: Optional[str] = Field(..., description="Diễn giải")
    transaction_num: Optional[str] = Field(..., description="Số bút toán")


class AccountFormRequest(BaseSchema):
    pay_in_form: AccountForm = Field(...)
    currency_exchange: CurrencyExchange = Field(..., description="Quy đổi ngoại tệ")
    currency_transfer: CurrencyTransfer = Field(..., description="Ngoại tệ chuyển ra nước ngoài")
    pay_in_account: PayInAccount = Field(..., description="Nộp tiền vào tài khoản")


class DepositPayInRequest(BaseSchema):
    # TODO
    account_form: AccountFormRequest = Field(...)
    fee_info: MultipleFeeInfoRequest = Field(..., description="Thông tin phí")
