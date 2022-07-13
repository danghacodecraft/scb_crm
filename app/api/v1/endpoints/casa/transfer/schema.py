from datetime import date
from typing import List, Optional, Union

from pydantic import Field, validator

from app.api.base.schema import ResponseRequestSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse
from app.utils.functions import is_valid_mobile_number
from app.utils.regex import (
    MAX_LENGTH_TRANSFER_CONTENT, REGEX_NUMBER_ONLY, REGEX_TRANSFER_CONTENT
)


class FeeInfoRequest(ResponseRequestSchema):
    is_transfer_payer: Optional[bool] = Field(
        ..., description="Bên thanh toán phí "
                         "<br/>`true`: Bên chuyển "
                         "<br/>`false`: Bên nhận "
                         "<br/>`null`: Không thu phí cùng giao dịch"
    )
    fee_amount: Optional[int] = Field(..., description="Số tiền phí")
    note: Optional[str] = Field(..., description="Ghi chú")


# Common
class CasaTransferCommonRequest(ResponseRequestSchema):
    sender_account_number: str = Field(..., description="Số tài khoản người chuyển khoản")
    sender_cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    sender_full_name_vn: Optional[str] = Field(None, description="Người giao dịch")
    sender_identity_number: Optional[str] = Field(None, description="Giấy tờ định danh")
    sender_issued_date: Optional[date] = Field(None, description="Ngày cấp")
    sender_place_of_issue: Optional[DropdownRequest] = Field(None, description="Nơi cấp")
    sender_address_full: Optional[str] = Field(None, description="Địa chỉ")
    sender_mobile_number: Optional[str] = Field(None, description="Số điện thoại", regex=REGEX_NUMBER_ONLY)
    receiving_method: str = Field(None, description="Hình thức nhận")
    is_fee: bool = Field(..., description="Có thu phí không")
    fee_info: Optional[FeeInfoRequest] = Field(..., description="Thông tin phí")
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")
    amount: int = Field(..., description="Số tiền")
    content: str = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )
    p_instrument_number: Optional[str] = Field(None, description="")
    core_fcc_request: Optional[str] = Field(None, description="")

    @validator("sender_mobile_number")
    def check_valid_mobile_number(cls, v):
        if not is_valid_mobile_number(v):
            raise TypeError('')
        return v


########################################################################################################################
# Thông tin người thụ hưởng
########################################################################################################################
class CasaTransferSCBToAccountRequest(CasaTransferCommonRequest):
    """
    Trong SCB đến tài khoản
    """
    receiver_account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)


class CasaTransferSCBByIdentityRequest(CasaTransferCommonRequest):
    """
    Trong SCB nhận bằng giấy tờ định danh
    """
    receiver_province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    receiver_branch: DropdownRequest = Field(..., description="Chi nhánh")
    receiver_full_name_vn: str = Field(..., description="Họ tên người thụ hưởng")
    receiver_identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    receiver_issued_date: date = Field(..., description="Ngày cấp")
    receiver_place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    receiver_mobile_number: Optional[str] = Field(..., description="Số điện thoại")
    receiver_address_full: Optional[str] = Field(..., description="Địa chỉ", max_length=500)

    @validator("receiver_mobile_number")
    def check_valid_mobile_number(cls, v):
        if not is_valid_mobile_number(v):
            raise TypeError('')
        return v


class CasaTransferThirdPartyRequest(CasaTransferCommonRequest):
    receiver_bank: DropdownRequest = Field(..., description="Ngân hàng")
    receiver_address_full: str = Field(..., description="Địa chỉ", max_length=100)


class CasaTransferThirdPartyToAccountRequest(CasaTransferThirdPartyRequest):
    """
    Ngoài SCB đến tài khoản
    """
    receiver_account_number: str = Field(..., description="Số tài khoản người thụ hưởng", regex=REGEX_NUMBER_ONLY)
    receiver_province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    receiver_full_name_vn: str = Field(..., description="Chủ tài khoản")


class CasaTransferThirdPartyByIdentityRequest(CasaTransferThirdPartyRequest):
    """
    Ngoài SCB nhận bằng giấy tờ định danh
    """
    receiver_branch: DropdownRequest = Field(..., description="Chi nhánh")
    receiver_province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    receiver_full_name_vn: str = Field(..., description="Chủ tài khoản")
    receiver_identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    receiver_issued_date: date = Field(..., description="Ngày cấp")
    receiver_place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    receiver_mobile_number: Optional[str] = Field(..., description="Số điện thoại")

    @validator("receiver_mobile_number")
    def check_valid_mobile_number(cls, v):
        if not is_valid_mobile_number(v):
            raise TypeError('')
        return v


class CasaTransferThirdParty247ToAccountRequest(CasaTransferThirdPartyRequest):
    """
    Ngoài SCB 24/7 tài khoản
    """
    receiver_account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    receiver_full_name: str = Field(None, description="Họ tên người nhận (Không cần truyền)")


class CasaTransferThirdParty247ToCardRequest(CasaTransferThirdPartyRequest):
    """
    Ngoài SCB 24/7 số thẻ
    """
    receiver_card_number: str = Field(..., description="Số thẻ")
    receiver_full_name: str = Field(None, description="Họ tên người nhận (Không cần truyền)")


class CasaTransferRequest(ResponseRequestSchema):
    receiving_method: str = Field(..., description="Hình thức nhận")
    data: Union[
        CasaTransferThirdPartyByIdentityRequest,
        CasaTransferSCBByIdentityRequest,
        CasaTransferThirdPartyToAccountRequest,
        CasaTransferThirdParty247ToAccountRequest,
        CasaTransferSCBToAccountRequest,
        CasaTransferThirdParty247ToCardRequest
    ] = Field(..., description="Nội dung")


########################################################################################################################
class DropdownCodeNameResponse(ResponseRequestSchema):
    code: Optional[str] = Field(..., description="Mã")
    name: Optional[str] = Field(..., description="Tên")


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
    place_of_issue: DropdownCodeNameResponse = Field(None, description="Nơi cấp")
    mobile_phone: Optional[str] = Field(None, description="Số điện thoại")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    currency: Optional[str] = Field(None, description="Loại tiền")


class TransferResponse(ResponseRequestSchema):
    amount: int = Field(..., description="Số tiền")
    content: str = Field(..., description="Nội dung chuyển tiền")
    entry_number: Optional[str] = Field(..., description="Số bút toán")


class FeeInfoResponse(ResponseRequestSchema):
    is_transfer_payer: bool = Field(..., description="`true`: Có thu phí cùng giao dịch, Bên thanh toán phí: Bên chuyển"
                                                     "`false`: Có thu phí cùng giao dịch, Bên thanh toán phí: Bên nhận"
                                                     "`null`: Không thu phí cùng giao dịch")
    payer: Optional[str] = Field(..., description="Bên thanh toán phí")
    fee_amount: Optional[int] = Field(..., description="Số tiền phí")
    vat_tax: Optional[float] = Field(..., description="Thuế VAT")
    total: Optional[float] = Field(..., description="Tổng số tiền phí")
    actual_total: Optional[float] = Field(..., description="Số tiền thực chuyển")
    note: Optional[str] = Field(..., description="Ghi chú")


class IdentityInfoResponse(ResponseRequestSchema):
    number: Optional[str] = Field(..., description="Số GTDD")
    issued_date: Optional[str] = Field(..., description="Ngày cấp")
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp")


class CustomerResponse(ResponseRequestSchema):
    account_number: str = Field(..., description="Tài khoản người chuyển tiền")
    cif_number: Optional[str] = Field(..., description="Số CIF")
    fullname_vn: Optional[str] = Field(..., description="Người giao dịch")
    address_full: Optional[str] = Field(..., description="Địa chỉ")
    identity_info: IdentityInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    mobile_phone: Optional[str] = Field(..., description="SĐT")
    telephone: Optional[str] = Field(..., description="SĐT")
    otherphone: Optional[str] = Field(..., description="SĐT")


class StaffInfoResponse(ResponseRequestSchema):
    code: Optional[str] = Field(..., description="Mã NV")
    name: Optional[str] = Field(..., description="Tên NV")


class CasaTransferResponse(ResponseRequestSchema):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: FeeInfoResponse = Field(..., description="Thông tin phí")
    sender: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")


class CasaTransferSourceAccountItemResponse(ResponseRequestSchema):
    number: str = Field(..., description="Số tài khoản thanh toán")
    fullname_vn: str = Field(..., description="Họ tên chủ thẻ")
    balance_available: float = Field(..., description="Số dư khả dụng")
    currency: str = Field(..., description="Loại tiền")
    account_type: str = Field(None, description="Loại tài khoản")


class CasaTransferSourceAccountListResponse(ResponseRequestSchema):
    total_items: int = Field(..., description="Tổng số tài khoản nguồn")
    casa_accounts: List[CasaTransferSourceAccountItemResponse] = Field(..., description="Danh sách tài khoản nguồn")
