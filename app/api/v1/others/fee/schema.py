from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.utils.constant.casa import CASA_FEE_METHODS
from app.utils.functions import make_description_from_dict


class FeeInfoRequest(BaseSchema):
    """
    Schema dùng chung cho phí
    """
    method_type: str = Field(..., description=f"Phương thức tính phí: {make_description_from_dict(CASA_FEE_METHODS)}")
    fee_id: Optional[str] = Field(..., description="Mã loại phí")
    amount: int = Field(..., description='Số tiền phí')
    content: str = Field(..., description='Nội dung')
    account_number: str = Field(..., description='STK')
