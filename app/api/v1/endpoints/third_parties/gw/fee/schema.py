from pydantic import Field

from app.api.base.schema import BaseGWSchema


class GWFeeInfoRequest(BaseGWSchema):
    product_name: str = Field(..., description="Tên loại sản phẩm phí")
    trans_amount: int = Field(..., description="Số tiền giao dịch")
    account_num: str = Field(..., description="Số tiền chịu phí")


class GWFeeInfoResponse(BaseGWSchema):
    charge_1: str = Field(..., description="Số tiền phí 1")
    charge_2: str = Field(..., description="Số tiền thuế của phí 1")
    charge_3: str = Field(None, description="Số tiền phí 2")
    charge_4: str = Field(None, description="Số tiền thuế của phí 2")
