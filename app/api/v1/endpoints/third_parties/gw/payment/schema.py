from pydantic import Field

from app.api.base.schema import BaseSchema


class AccountAmountBlock(BaseSchema):
    amount: int = Field(..., description="Số dư bị phong tỏa")
    amount_block_type: str = Field(..., description="Loại phong tỏa")
    hold_code: str = Field(..., description="Mã lý do bị phong tỏa")
    effective_date: str = Field(..., description="Ngày hiệu lực phong tỏa")
    expiry_date: str = Field(None, description="Ngày hết hiệu lực phong tỏa")
    remarks: str = Field(..., description="Ghi chú")
    verify_available_balance: str = Field(
        ...,
        description="Có hoặc không kiểm tra giá trị số dư trước khi phong tỏa. Giá trị Y/N"
    )
