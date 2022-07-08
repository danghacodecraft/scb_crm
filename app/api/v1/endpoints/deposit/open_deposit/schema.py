from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField


class TdAccountRequest(BaseSchema):
    currency_id: str = Field(..., description='Loại tiền')
    account_type_id: str = Field(..., description='Loại nhóm sản phẩm (gói) tài khoản')
    account_class_id: str = Field(..., description='Loại hình tài khoản')
    amount: Optional[int] = Field(None, description='Số dư hiện tại')
    pay_in_amount: int = Field(..., description='Thông tin nguồn tiền đầu vào')
    pay_in_casa_account: Optional[str] = Field(None, description='Tài khoản nguồn tiền đầu vào')
    pay_out_interest_casa_account: str = Field(..., description='Tài khoản nhận lãi')
    pay_out_casa_account: str = Field(..., description='Tài khoản nhận gốc')
    td_contract_num: str = Field(..., description='Số hợp đồng')
    fcc_transaction_num: str = Field(None, description='Số bút toán (FCC)')
    maturity_date: date = Field(..., description='Ngày đáo hạn')
    td_serial: str = Field(..., description='Số serial')
    td_interest_type: str = Field(..., description='Hình thức lãi')
    td_interest: str = Field(..., description='Lãi suất tiết kiệm')
    td_rollover_type: Optional[str] = Field(..., description='Chỉ định khi đến hạn:I = Tái ký gốc + lãi ,P = Tái ký gốc')
    pay_out_casa_account_resign: Optional[str] = Field(..., description='Tài khoản nhận lãi tái ký')
    td_interest_class_resign: Optional[str] = Field(..., description='Hình thức lãi tái ký')
    acc_class_id_resign: Optional[str] = Field(..., description='Loại hình tài khoản tái ký')
    acc_type_id_resign: Optional[str] = Field(..., description='Loại nhóm sản phẩm (gói) tài khoản tái ký')


class DepositOpenTDAccountRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    td_account: List[TdAccountRequest] = Field(..., description="Danh sách TKTK")
