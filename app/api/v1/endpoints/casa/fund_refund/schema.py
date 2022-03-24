from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


# --  A. ỨNG QUỸ/HOÀN QUỸ  ------------------------------------
# I. Loại giao dịch
class SealedBagResponse(BaseSchema):
    id: str = Field(..., description="ID bao niêm phong của từng user thuộc đơn vị")
    code: str = Field(..., description="Code bao niêm phong của từng user thuộc đơn vị")
    name: str = Field(..., description="Name bao niêm phong của từng user thuộc đơn vị")
    amount: int = Field(..., description="Số tiền tương ứng trên bao niêm phong")
    status: DropdownResponse = Field(..., description="Trạng thái bao niêm phong")


class SealedBagRequest(BaseSchema):
    id: str = Field(..., description="Bao niêm phong của từng user thuộc đơn vị")
    amount: int = Field(..., description="Số tiền tương ứng trên bao niêm phong")
    status: DropdownRequest = Field(..., description="Trạng thái bao niêm phong")  # TODO: thêm selected_flag


class TransactionTypeResponse(BaseSchema):
    is_fund_flag: bool = Field(True, description="Cờ chọn loại giao dịch: `true` - Ứng quỹ, `false`: Hoàn quỹ")  # TODO: required
    is_main_fund_flag: bool = Field(True, description="Cờ chọn quỹ cần ứng/ hoàn: `true` - Quỹ chính, `false` - Quỹ phụ")  # TODO: required
    till_or_vault: DropdownResponse = Field(..., description="Till/Vault ID ứng quỹ/ hoàn quỹ")
    full_name_vn: str = Field(..., description="Họ và tên người thực hiện ứng quỹ/ hoàn quỹ")
    position: DropdownResponse = Field(..., description="Chức vụ người thực hiện ứng quỹ/ hoàn quỹ")
    currency: DropdownResponse = Field(..., description="Chọn loại tiền ứng quỹ/ hoàn quỹ")
    amount: int = Field(..., description="Số tiền cần ứng/ hoàn quỹ")
    content: str = Field(None, description="Nội dung hoàn/ ứng quỹ")
    automatic_declaration_flag: bool = Field(False, description="Cờ kê tự động")  # TODO: Kê tự động là 1 API
    sealed_bags: List[SealedBagResponse] = Field(..., description="Danh sách bao niêm phong ứng quỹ/ hoàn quỹ")


class TransactionTypeRequest(BaseSchema):
    is_fund_flag: bool = Field(True, description="Cờ chọn loại giao dịch: `true` - Ứng quỹ, `false`: Hoàn quỹ")
    is_main_fund_flag: bool = Field(True, description="Cờ chọn quỹ cần ứng/ hoàn: `true` - Quỹ chính, `false` - Quỹ phụ")
    till_or_vault: DropdownRequest = Field(..., description="Till/Vault ID ứng quỹ/ hoàn quỹ")
    full_name_vn: str = Field(..., description="Họ và tên người thực hiện ứng quỹ/ hoàn quỹ")
    position: DropdownRequest = Field(..., description="Chức vụ người thực hiện ứng quỹ/ hoàn quỹ")
    currency: DropdownRequest = Field(..., description="Chọn loại tiền ứng quỹ/ hoàn quỹ")
    amount: int = Field(..., description="Số tiền cần ứng/ hoàn quỹ")
    content: str = Field(None, description="Nội dung hoàn/ ứng quỹ")  # TODO: tất cả string type minlength = 1
    sealed_bags: List[SealedBagRequest] = Field(..., description="Danh sách bao niêm phong ứng quỹ/ hoàn quỹ")


class InvoiceItemResponse(BaseSchema):
    denomination: int = Field(..., description="Mệnh giá tiền")
    quantity: int = Field(..., description="Số lượng")
    total: int = Field(0, description="Tổng cộng")


class InvoiceItemRequest(BaseSchema):
    denomination: int = Field(..., description="Mệnh giá tiền")
    quantity: int = Field(..., description="Số lượng")


class InvoiceListDetailResponse(BaseSchema):
    invoice_list: List[InvoiceItemResponse] = Field(..., description="Bảng kê")
    total_list: int = Field(0, description="Tổng số tiền mục thành tiền bảng kê")
    total_sealed_bags: int = Field(0, description="Tổng số tiền dựa trên bao niêm phong được chọn")
    total_money: int = Field(0, description="Tổng thành tiền")


class InvoiceListDetailRequest(BaseSchema):
    invoice_list: List[InvoiceItemRequest] = Field(..., description="Bảng kê")
    total_list: int = Field(0, description="Tổng số tiền mục thành tiền bảng kê")  # TODO: bỏ
    total_sealed_bags: int = Field(0, description="Tổng số tiền dựa trên bao niêm phong được chọn")
    total_money: int = Field(0, description="Tổng thành tiền")


class FundRefundResponse(BaseSchema):
    transaction_code: str = Field(..., description="Mã giao dịch")
    transaction_type: TransactionTypeResponse = Field(..., description="Loại giao dịch")
    invoice_list_detail: InvoiceListDetailResponse = Field(..., description="Chi tiết bảng kê")  # TODO: invoice_details

########################################################################################################################
# Resquest
########################################################################################################################
########################################################################################################################
# Response
########################################################################################################################


class FundRefundRequest(BaseSchema):
    transaction_code: str = Field(..., description="Mã giao dịch")
    transaction_type: TransactionTypeRequest = Field(..., description="Loại giao dịch")
    invoice_list_detail: InvoiceListDetailRequest = Field(..., description="Chi tiết bảng kê")
