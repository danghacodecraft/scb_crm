from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


########################################################################################################################
# Response
########################################################################################################################
class SealedBagResponse(BaseSchema):
    id: str = Field(..., min_length=1, description="ID bao niêm phong của từng user thuộc đơn vị")
    code: str = Field(..., min_length=1, description="Code bao niêm phong của từng user thuộc đơn vị")
    name: str = Field(..., min_length=1, description="Name bao niêm phong của từng user thuộc đơn vị")
    amount: int = Field(..., description="Số tiền tương ứng trên bao niêm phong")
    status: DropdownResponse = Field(..., description="Trạng thái bao niêm phong")
    selected_flag: bool = Field(..., description="Cờ chọn bao niêm phong")


class TransactionTypeResponse(BaseSchema):
    is_fund_flag: bool = Field(..., description="Cờ chọn loại giao dịch: `true` - Ứng quỹ, `false`: Hoàn quỹ")
    is_main_fund_flag: bool = Field(..., description="Cờ chọn quỹ cần ứng/ hoàn: `true` - Quỹ chính, `false` - Quỹ phụ")
    till_or_vault: DropdownResponse = Field(..., description="Till/Vault ID ứng quỹ/ hoàn quỹ")
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên người thực hiện ứng quỹ/ hoàn quỹ")
    position: DropdownResponse = Field(..., description="Chức vụ người thực hiện ứng quỹ/ hoàn quỹ")
    currency: DropdownResponse = Field(..., description="Chọn loại tiền ứng quỹ/ hoàn quỹ")
    amount: int = Field(..., description="Số tiền cần ứng/ hoàn quỹ")
    content: str = Field(None, min_length=1, description="Nội dung hoàn/ ứng quỹ")
    sealed_bags: List[SealedBagResponse] = Field(..., description="Danh sách bao niêm phong ứng quỹ/ hoàn quỹ")


class InvoiceItemResponse(BaseSchema):
    denomination: int = Field(..., description="Mệnh giá tiền")
    quantity: int = Field(..., description="Số lượng")
    total: int = Field(..., description="Tổng cộng")


class InvoiceDetailsResponse(BaseSchema):
    invoice_list: List[InvoiceItemResponse] = Field(..., description="Bảng kê")
    total_list: int = Field(..., description="Tổng số tiền mục thành tiền bảng kê")
    total_sealed_bags: int = Field(..., description="Tổng số tiền dựa trên bao niêm phong được chọn")
    total_money: int = Field(..., description="Tổng thành tiền")


class FundRefundResponse(BaseSchema):
    transaction_code: str = Field(..., min_length=1, description="Mã giao dịch")
    transaction_type: TransactionTypeResponse = Field(..., description="Loại giao dịch")
    invoice_details: InvoiceDetailsResponse = Field(..., description="Chi tiết bảng kê")


########################################################################################################################
# Resquest
########################################################################################################################
class SealedBagRequest(BaseSchema):
    id: str = Field(..., min_length=1, description="Bao niêm phong của từng user thuộc đơn vị")
    amount: int = Field(..., description="Số tiền tương ứng trên bao niêm phong")
    status: DropdownRequest = Field(..., description="Trạng thái bao niêm phong")
    selected_flag: bool = Field(..., description="Cờ chọn bao niêm phong")


class TransactionTypeRequest(BaseSchema):
    is_fund_flag: bool = Field(..., description="Cờ chọn loại giao dịch: `true` - Ứng quỹ, `false`: Hoàn quỹ")
    is_main_fund_flag: bool = Field(..., description="Cờ chọn quỹ cần ứng/ hoàn: `true` - Quỹ chính, `false` - Quỹ phụ")
    till_or_vault: DropdownRequest = Field(..., description="Till/Vault ID ứng quỹ/ hoàn quỹ")
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên người thực hiện ứng quỹ/ hoàn quỹ")
    position: DropdownRequest = Field(..., description="Chức vụ người thực hiện ứng quỹ/ hoàn quỹ")
    currency: DropdownRequest = Field(..., description="Chọn loại tiền ứng quỹ/ hoàn quỹ")
    amount: int = Field(..., description="Số tiền cần ứng/ hoàn quỹ")
    content: str = Field(None, min_length=1, description="Nội dung hoàn/ ứng quỹ")
    sealed_bags: List[SealedBagRequest] = Field(..., description="Danh sách bao niêm phong ứng quỹ/ hoàn quỹ")


class InvoiceItemRequest(BaseSchema):
    denomination: int = Field(..., description="Mệnh giá tiền")
    quantity: int = Field(..., description="Số lượng")


class InvoiceDetailsRequest(BaseSchema):
    invoice_list: List[InvoiceItemRequest] = Field(..., description="Bảng kê")


class FundRefundRequest(BaseSchema):
    transaction_code: str = Field(..., min_length=1, description="Mã giao dịch")
    transaction_type: TransactionTypeRequest = Field(..., description="Loại giao dịch")
    invoice_details: InvoiceDetailsRequest = Field(..., description="Chi tiết bảng kê")
