from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.casa.schema import (
    SenderInfoRequest, SenderInfoResponse, StatementInfoRequest
)
from app.utils.constant.casa import CASA_FEE_METHODS, DENOMINATIONS__AMOUNTS
from app.utils.functions import (
    make_description_from_dict, make_description_from_dict_to_list
)


class AccountInfoResponse(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    sec_amount: int = Field(..., description="Số cuốn")
    sec_unit_amount: int = Field(..., description="Số tờ")


class OpenSecFeeInfoResponse(BaseSchema):
    method: str = Field(..., description=f"Hình thức: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: Optional[str] = Field(..., description="`CASA` => Số tài khoản, `CASH` => null")
    amount: int = Field(..., description="Số tiền phí")
    vat: int = Field(..., description="Thuế VAT")
    total: int = Field(..., description="Tổng phí")


class StatementDetailInfoResponse(BaseSchema):
    denominations: str = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")
    into_money: int = Field(..., description="Thành tiền")


class StatementInfoResponse(BaseSchema):
    statements: List[StatementDetailInfoResponse]
    total: int = Field(..., description="Tổng thành tiền")


class TransactionInfoResponse(BaseSchema):
    total_sec_amount: int = Field(..., description="Tổng số cuốn")
    total_sec_unit_amount: int = Field(..., description="Tổng số tờ")
    content: str = Field(..., description="Nội dung")
    ref_number: str = Field(None, description="Số bút toán")  # TODO: tìm số bút toán
    fee_info: OpenSecFeeInfoResponse = Field(..., description="II. Thông tin phí")
    statement: StatementInfoResponse = Field(..., description="III. Bảng kê tiền giao dịch")
    sender: SenderInfoResponse = Field(..., description="IV. Thông tin khách hàng giao dịch")


class OpenSecResponse(BaseSchema):
    account_infos: List[AccountInfoResponse] = Field(..., description="Thông tin tài khoản")
    transaction_info: TransactionInfoResponse = Field(..., description="Thông tin giao dịch và phí")
    note: Optional[str] = Field(..., description="Ghi chú")


class OpenSecAccountRequest(BaseSchema):
    account_number: str = Field(..., description="Số tài khoản")
    sec_amount: int = Field(..., description="Số cuốn")


class OpenSecFeeInfoRequest(BaseSchema):
    method: str = Field(..., description=f"Hình thức: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: Optional[str] = Field(..., description="`CASA` => Số tài khoản, `CASH` => null")
    amount: int = Field(..., description="Số tiền phí")
    vat: int = Field(..., description="Thuế VAT")


class OpenSecTransactionInfoRequest(BaseSchema):
    content: str = Field(..., description="Nội dung")
    fee_info: Optional[OpenSecFeeInfoRequest] = Field(
        ..., description="Có thu phí => Truyền data, Không thu phí => fee_info=null")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    sender: SenderInfoRequest = Field(..., description="Thông tin khách hàng giao dịch")


class OpenSecRequest(BaseSchema):
    account_infos: List[OpenSecAccountRequest] = Field(..., description="Danh sách tài khoản")
    transaction_info: OpenSecTransactionInfoRequest = Field(..., description="Thông tin giao dịch")
    note: Optional[str] = Field(..., description="Ghi chú")
