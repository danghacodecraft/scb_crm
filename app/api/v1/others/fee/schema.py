from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse
from app.utils.constant.casa import CASA_FEE_METHODS
from app.utils.functions import make_description_from_dict


class FeeDetailInfoRequest(BaseSchema):
    fee_id: Optional[str] = Field(..., description="Mã loại phí")
    amount: int = Field(..., description='Số tiền phí')
    content: str = Field(..., description='Nội dung')
    account_number: str = Field(..., description='STK')


class FeeInfoRequest(BaseSchema):
    """
    Schema dùng chung cho phí
    """
    method_type: str = Field(..., description=f"Phương thức tính phí: {make_description_from_dict(CASA_FEE_METHODS)}")
    fee_details: List[FeeDetailInfoRequest] = Field(..., description="Danh sách phí")


class FeeDetailInfoResponse(BaseSchema):
    fee_category: DropdownResponse = Field(..., description="Nhóm phí")
    fee: DropdownResponse = Field(..., description="Mã loại phí")
    amount: int = Field(..., description='Số tiền phí')
    vat: int = Field(..., description='Thuế VAT')
    total: int = Field(..., description='Tổng phí')
    content: str = Field(..., description='Nội dung')
    ref_num: str = Field(..., description='Số bút toán')


class FeeInfoResponse(BaseSchema):
    method_type: str = Field(..., description=f"Phương thức tính phí: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: str = Field(..., description='STK')
    account_owner: str = Field(..., description="Chủ tài khoản")
    fee_details: List[FeeDetailInfoResponse] = Field(..., description="Danh sách phí")
    total_fee: int = Field(..., description="Tổng phí")
