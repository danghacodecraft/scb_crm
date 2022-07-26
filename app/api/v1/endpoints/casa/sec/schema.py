from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, ResponseRequestSchema
from app.utils.constant.casa import DENOMINATIONS__AMOUNTS
from app.utils.functions import make_description_from_dict_to_list


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


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")


class SenderInfoRequest(BaseSchema):
    cif_flag: bool = Field(..., description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
    cif_number: Optional[str] = Field(None, description="Số CIF")
    fullname_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: Optional[str] = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_phone: Optional[str] = Field(None, description="SĐT")
    telephone: Optional[str] = Field(None, description="SĐT")
    otherphone: Optional[str] = Field(None, description="SĐT")


class TransactionInfoFees(BaseSchema):
    transaction_info: TransactionInfoRequest = Field(..., description="I. Thông tin giao dịch")
    fee_info: FeeInfoRequest = Field(..., description="II. Thông tin phí")
    statement: List[StatementInfoRequest] = Field(..., description="III. Bảng kê tiền giao dịch")
    sender_info: SenderInfoRequest = Field(..., description="IV. Thông tin khách hàng giao dịch")


class SecRequest(BaseSchema):
    basic_info: BasiInfoRequest = Field(..., description="Thông tin cơ bản")
    transaction_info_fees: TransactionInfoFees = Field(..., description="Thông tin giao dịch và phí")
