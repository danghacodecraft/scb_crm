from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse
from app.utils.constant.casa import CASA_FEE_METHODS, PAYMENT_PAYERS
from app.utils.functions import make_description_from_dict


class FeeDetailInfoRequest(BaseSchema):
    fee_id: Optional[str] = Field(..., description="Mã loại phí")
    amount: int = Field(..., description='Số tiền phí')
    content: str = Field(..., description='Nội dung')


class MultipleFeeInfoRequest(BaseSchema):
    """
    Schema dùng chung cho phí
    """
    method_type: str = Field(..., description=f"Phương thức tính phí: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: str = Field(..., description='STK')
    fee_details: List[FeeDetailInfoRequest] = Field(..., description="Danh sách phí")


class FeeDetailInfoResponse(BaseSchema):
    payer: Optional[str] = Field(None, description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field(None, description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field(None, description="Mã loại phí")
    amount: int = Field(..., description='Số tiền phí')
    vat: int = Field(..., description='Thuế VAT')
    total: int = Field(..., description='Tổng phí')
    actual_total: Optional[float] = Field(None, description="Số tiền thực chuyển")
    content: str = Field(None, description='Nội dung')
    ref_num: str = Field(None, description='Số bút toán')


class FeeInfoResponse(BaseSchema):
    method_type: str = Field(..., description=f"Phương thức tính phí: {make_description_from_dict(CASA_FEE_METHODS)}")
    account_number: str = Field(..., description='STK')
    account_owner: str = Field(..., description="Chủ tài khoản")
    fee_details: List[FeeDetailInfoResponse] = Field(..., description="Danh sách phí")
    total_fee: int = Field(..., description="Tổng phí")


class OneFeeInfoRequest(BaseSchema):
    payer: str = Field(..., description=f"{make_description_from_dict(PAYMENT_PAYERS)}")
    amount: int = Field(..., description="Số tiền phí")
    note: Optional[str] = Field(..., description="Ghi chú")
