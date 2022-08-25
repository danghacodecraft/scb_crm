from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import (
    ResponseRequestSchema, TMSCreatedUpdatedBaseModel
)
from app.api.v1.endpoints.approval_v2.template.schema import (
    DropdownCodeNameResponse, FeeDetailInfoResponse, StaffInfoResponse
)
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse


class IdentityInfoResponse(ResponseRequestSchema):
    number: Optional[str] = Field(..., description="Số GTDD")
    issued_date: Optional[str] = Field(..., description="Ngày cấp")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class CustomerResponse(ResponseRequestSchema):
    account_number: str = Field(..., description="Tài khoản người chuyển tiền")
    cif_number: Optional[str] = Field(..., description="Số CIF")
    fullname_vn: Optional[str] = Field(..., description="Người giao dịch")
    address_full: Optional[str] = Field(..., description="Địa chỉ")
    identity_info: IdentityInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    mobile_phone: Optional[str] = Field(..., description="SĐT")
    telephone: Optional[str] = Field(..., description="SĐT")
    otherphone: Optional[str] = Field(..., description="SĐT")


class TransferResponse(ResponseRequestSchema):
    amount: str = Field(..., description="Số tiền")
    content: str = Field(..., description="Nội dung chuyển tiền")
    entry_number: Optional[str] = Field(..., description="Số bút toán")


class TransferTypeResponse(ResponseRequestSchema):
    receiving_method_type: Optional[str] = Field(..., description="Loại")
    receiving_method: Optional[str] = Field(..., description="Hình thức nhận")


class ReceiverResponse(ResponseRequestSchema):
    account_number: Optional[str] = Field(None, description="Số tài khoản người nhận")
    card_number: Optional[str] = Field(None, description="Số thẻ người nhận")
    fullname_vn: Optional[str] = Field(None, description="Chủ tài khoản")
    bank: DropdownCodeNameResponse = Field(None, description="Ngân hàng")
    province: DropdownCodeNameResponse = Field(None, description="Tỉnh/Thành phố")
    branch_info: DropdownCodeNameResponse = Field(None, description="Đơn vị thụ hưởng")
    identity_number: Optional[str] = Field(None, description="Số giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: DropdownResponse = Field(None, description="Nơi cấp")
    mobile_phone: Optional[str] = Field(None, description="Số điện thoại")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    currency: Optional[str] = Field(None, description="Loại tiền")


class TMSCasaTransferResponse(TMSCreatedUpdatedBaseModel):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: FeeDetailInfoResponse = Field(None, description="Thông tin phí")
    sender: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
