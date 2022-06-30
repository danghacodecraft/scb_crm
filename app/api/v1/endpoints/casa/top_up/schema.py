from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import ResponseRequestSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest
from app.utils.constant.casa import DENOMINATIONS__AMOUNTS
from app.utils.functions import make_description_from_dict_to_list
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
    fee_amount: int = Field(..., description="Số tiền phí")
    note: Optional[str] = Field(..., description="Ghi chú")


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")


# Common
class TopUpRequest(ResponseRequestSchema):
    cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    receiving_method: str = Field(..., description="Hình thức nhận")
    is_fee: bool = Field(..., description="Có thu phí không")
    fee_info: Optional[FeeInfoRequest] = Field(..., description="Thông tin phí")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")


########################################################################################################################
# Thông tin người thụ hưởng
########################################################################################################################
class TopUpSCBToAccountRequest(TopUpRequest):
    """
    Trong SCB đến tài khoản
    """
    account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    amount: int = Field(..., description="Số tiền")
    content: Optional[str] = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )


class TopUpSCBByIdentity(TopUpRequest):
    """
    Trong SCB nhận bằng giấy tờ định danh
    """
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    branch: DropdownRequest = Field(..., description="Chi nhánh")
    full_name_vn: str = Field(..., description="Họ tên người thụ hưởng")
    identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    mobile_number: Optional[str] = Field(..., description="Số điện thoại")
    address_full: Optional[str] = Field(..., description="Địa chỉ", max_length=500)
    amount: int = Field(..., description="Số tiền")
    content: str = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )


class TopUpThirdPartyToAccount(TopUpRequest):
    """
    Ngoài SCB đến tài khoản
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    branch: DropdownRequest = Field(..., description="Chi nhánh")
    full_name_vn: str = Field(..., description="Chủ tài khoản")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


class TopUpThirdPartyByIdentity(TopUpRequest):
    """
    Ngoài SCB nhận bằng giấy tờ định danh
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    branch: DropdownRequest = Field(..., description="Chi nhánh")
    full_name_vn: str = Field(..., description="Chủ tài khoản")
    identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    mobile_number: Optional[str] = Field(..., description="Số điện thoại")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


class TopUpThirdParty247ToAccount(TopUpRequest):
    """
    Ngoài SCB 24/7 tài khoản
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


class TopUpThirdParty247ToCard(TopUpRequest):
    """
    Ngoài SCB 24/7 số thẻ
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    card_number: str = Field(..., description="Số thẻ")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


########################################################################################################################
class DropdownCodeNameResponse(ResponseRequestSchema):
    code: Optional[str] = Field(..., description="Mã")
    name: Optional[str] = Field(..., description="Tên")


class TransferTypeResponse(ResponseRequestSchema):
    receiving_method_type: Optional[str] = Field(..., description="Loại")
    receiving_method: Optional[str] = Field(..., description="Hình thức nhận")


class ReceiverResponse(ResponseRequestSchema):
    account_number: Optional[str] = Field(None, description="Số tài khoản")
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
    content: Optional[str] = Field(..., description="Nội dung chuyển tiền")
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


class StatementsResponse(ResponseRequestSchema):
    denominations: Optional[str] = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")


class StatementResponse(ResponseRequestSchema):
    statements: List[StatementsResponse] = Field(..., description="Thông tin chi tiết bảng kê")
    total: int = Field(..., description="Tổng thành tiền")
    odd_difference: float = Field(..., description="Chênh lệch lẻ")


class IdentityInfoResponse(ResponseRequestSchema):
    number: Optional[str] = Field(..., description="Số GTDD")
    issued_date: Optional[str] = Field(..., description="Ngày cấp")
    place_of_issue: Optional[str] = Field(..., description="Nơi cấp")


class CustomerResponse(ResponseRequestSchema):
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


class TopUpResponse(ResponseRequestSchema):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: FeeInfoResponse = Field(..., description="Thông tin phí")
    statement: StatementResponse = Field(..., description="Thông tin bảng kê")
    customer: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
