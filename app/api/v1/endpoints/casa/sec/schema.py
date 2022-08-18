from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.casa.schema import (
    SenderInfoRequest, SenderInfoResponse, StatementInfoRequest
)
from app.api.v1.others.fee.schema import (
    FeeInfoResponse, MultipleFeeInfoRequest
)
from app.api.v1.others.statement.schema import StatementResponse


class AccountInfoResponse(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    sec_amount: int = Field(..., description="Số cuốn")
    sec_unit_amount: int = Field(..., description="Số tờ")


class OpenSecAccountRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    sec_amount: int = Field(..., description="Số cuốn")


class TransactionInfoResponse(BaseSchema):
    total_sec_amount: int = Field(..., description="Tổng số cuốn")
    total_sec_unit_amount: int = Field(..., description="Tổng số tờ")
    content: str = Field(..., description="Nội dung")
    ref_number: str = Field(None, description="Số bút toán")  # TODO: tìm số bút toán
    fee_info: Optional[FeeInfoResponse] = Field(..., description="II. Thông tin phí")
    statements: StatementResponse = Field(..., description="III. Bảng kê tiền giao dịch")
    sender: SenderInfoResponse = Field(..., description="IV. Thông tin khách hàng giao dịch")


class OpenSecResponse(BaseSchema):
    account_infos: List[AccountInfoResponse] = Field(..., description="Thông tin tài khoản")
    transaction_info: TransactionInfoResponse = Field(..., description="Thông tin giao dịch và phí")
    note: Optional[str] = Field(..., description="Ghi chú")


class OpenSecTransactionInfoRequest(BaseSchema):
    content: str = Field(..., description="Nội dung")
    fee_info: Optional[MultipleFeeInfoRequest] = Field(
        ..., description="Có thu phí => Truyền data, Không thu phí => fee_info=null")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    sender: SenderInfoRequest = Field(..., description="Thông tin khách hàng giao dịch")


class OpenSecRequest(BaseSchema):
    account_infos: List[OpenSecAccountRequest] = Field(..., description="Danh sách tài khoản")
    transaction_info: OpenSecTransactionInfoRequest = Field(..., description="Thông tin giao dịch")
    note: Optional[str] = Field(..., description="Ghi chú")
