from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.casa.schema import (
    SenderInfoRequest, StatementInfoRequest
)
from app.utils.constant.casa import CASA_FEE_METHODS
from app.utils.functions import make_description_from_dict


class BasiInfoRequest(BaseSchema):
    sec_number: int = Field(..., description="Số cuốn")


class TransactionInfoRequest(BaseSchema):
    content: str = Field(..., description="Nội dung")


class FeeInfoRequest(BaseSchema):
    is_transfer_payer: bool = Field(
        ...,
        description=' 1. Cờ có thu phí hay không, `true`: Có thu phí, `false` = Không thu phí'
    )
    payer_flag: Optional[bool] = Field(None,
                                       description="2. Hình thức, `true`: Tiền mặt, `false` = Tài khoản thanh toán'")
    account_number: Optional[str] = Field(..., description="Số tài khoản")
    amount: Optional[int] = Field(None, description="3. Số tiền phí")


class TransactionInfoFees(BaseSchema):
    transaction_info: TransactionInfoRequest = Field(..., description="I. Thông tin giao dịch")
    fee_info: FeeInfoRequest = Field(..., description="II. Thông tin phí")
    statement: List[StatementInfoRequest] = Field(..., description="III. Bảng kê tiền giao dịch")
    sender_info: SenderInfoRequest = Field(..., description="IV. Thông tin khách hàng giao dịch")


class SaveSecResponse(BaseSchema):
    basic_info: BasiInfoRequest = Field(..., description="Thông tin cơ bản")
    transaction_info_fees: TransactionInfoFees = Field(..., description="Thông tin giao dịch và phí")


class SaveSecAccountRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    sec_amount: int = Field(..., description="Số cuốn")


class SaveSecFeeInfoRequest(BaseSchema):
    method: str = Field(..., description=f"Hình thức: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: Optional[str] = Field(..., description="`CASA` => Số tài khoản, `CASH` => null")
    amount: int = Field(..., description="Số tiền phí")
    vat: int = Field(..., description="Thuế VAT")


class SaveSecTransactionInfoRequest(BaseSchema):
    content: str = Field(..., description="Nội dung")
    fee_info: Optional[SaveSecFeeInfoRequest] = Field(
        ..., description="Có thu phí => Truyền data, Không thu phí => fee_info=null")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    sender: SenderInfoRequest


class SaveSecRequest(BaseSchema):
    account_infos: List[SaveSecAccountRequest] = Field(..., description="Danh sách tài khoản")
    transaction_info: SaveSecTransactionInfoRequest = Field(..., description="Thông tin giao dịch")
    note: Optional[str] = Field(..., description="Ghi chú")
