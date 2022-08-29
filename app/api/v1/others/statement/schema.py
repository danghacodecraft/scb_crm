from typing import List, Optional

from pydantic import Field

from app.api.base.schema import ResponseRequestSchema


class StatementDetailInfo(ResponseRequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: int = Field(..., description="Số lượng")


class StatementInfoRequest(ResponseRequestSchema):
    statement_type: str = Field(..., description="Loại bảng kê")
    currency_type: str = Field(..., description="Loại bảng kê")
    statement_detail: List[StatementDetailInfo] = Field(..., description="Chi tiết bảng kê")


class StatementsResponse(ResponseRequestSchema):
    denominations: Optional[str] = Field(..., description="Mệnh giá")
    amount: int = Field(..., description="Số lượng")
    into_money: int = Field(..., description="Thành tiền")


class StatementResponse(ResponseRequestSchema):
    statements: List[StatementsResponse] = Field(..., description="Thông tin chi tiết bảng kê")
    total: int = Field(..., description="Tổng thành tiền")
    odd_difference: float = Field(..., description="Chênh lệch lẻ")
    statement_type: str = Field(..., description="Loại bảng kê")
    currency_type: str = Field(..., description="Loại bảng kê")
