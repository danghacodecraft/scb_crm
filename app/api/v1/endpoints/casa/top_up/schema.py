from datetime import date
from typing import List, Optional, Union

from pydantic import Field, validator

from app.api.base.schema import ResponseRequestSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse
from app.utils.constant.casa import DENOMINATIONS__AMOUNTS, RECEIVING_METHODS
from app.utils.functions import (
    is_valid_mobile_number, make_description_from_dict,
    make_description_from_dict_to_list
)
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


class StatementInfoRequest(ResponseRequestSchema):
    denominations: str = Field(
        ..., description=f"Mệnh giá: {make_description_from_dict_to_list(DENOMINATIONS__AMOUNTS)}"
    )
    amount: int = Field(..., description="Số lượng")


# Common
class CasaTopUpCommonRequest(ResponseRequestSchema):
    sender_cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    sender_full_name_vn: Optional[str] = Field(None, description="Người giao dịch")
    sender_identity_number: Optional[str] = Field(None, description="Giấy tờ định danh")
    sender_issued_date: Optional[date] = Field(None, description="Ngày cấp")
    sender_place_of_issue: Optional[DropdownRequest] = Field(None, description="Nơi cấp")
    sender_address_full: Optional[str] = Field(None, description="Địa chỉ")
    sender_mobile_number: Optional[str] = Field(None, description="Số điện thoại", regex=REGEX_NUMBER_ONLY)
    receiving_method: str = Field(None, description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}")
    is_fee: bool = Field(..., description="Có thu phí không")
    fee_info: Optional[FeeInfoRequest] = Field(..., description="Thông tin phí")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
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
class CasaTopUpSCBToAccountRequest(CasaTopUpCommonRequest):
    """
    Trong SCB đến tài khoản
    """
    receiver_account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)


class CasaTopUpSCBByIdentityRequest(CasaTopUpCommonRequest):
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


class CasaTopUpThirdPartyCommonRequest(CasaTopUpCommonRequest):
    receiver_bank: DropdownRequest = Field(..., description="Ngân hàng")
    receiver_address_full: str = Field(..., description="Địa chỉ", max_length=100)


class CasaTopUpThirdPartyToAccountRequest(CasaTopUpThirdPartyCommonRequest):
    """
    Ngoài SCB đến tài khoản
    """
    receiver_province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    receiver_account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    receiver_full_name_vn: str = Field(..., description="Chủ tài khoản")


class CasaTopUpThirdPartyByIdentityRequest(CasaTopUpThirdPartyCommonRequest):
    """
    Ngoài SCB nhận bằng giấy tờ định danh
    """
    receiver_province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    receiver_bank_branch: str = Field(..., description="Chi nhánh ngân hàng")
    receiver_full_name_vn: str = Field(..., description="Chủ tài khoản")
    receiver_identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    receiver_issued_date: date = Field(..., description="Ngày cấp")
    receiver_place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    receiver_mobile_number: Optional[str] = Field(None, description="Số điện thoại")

    @validator("receiver_mobile_number")
    def check_valid_mobile_number(cls, v):
        if not is_valid_mobile_number(v):
            raise TypeError('')
        return v


class CasaTopUpThirdParty247ToAccountRequest(CasaTopUpThirdPartyCommonRequest):
    """
    Ngoài SCB 24/7 tài khoản
    """
    receiver_account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)


class CasaTopUpThirdParty247ToCardRequest(CasaTopUpThirdPartyCommonRequest):
    """
    Ngoài SCB 24/7 số thẻ
    """
    receiver_card_number: str = Field(..., description="Số thẻ")


class CasaTopUpRequest(ResponseRequestSchema):
    receiving_method: str = Field(..., description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}")
    data: Union[
        CasaTopUpThirdPartyByIdentityRequest,
        CasaTopUpSCBByIdentityRequest,
        CasaTopUpThirdPartyToAccountRequest,
        CasaTopUpThirdParty247ToAccountRequest,
        CasaTopUpSCBToAccountRequest,
        CasaTopUpThirdParty247ToCardRequest
    ] = Field(..., description="Nội dung")


########################################################################################################################
class DropdownCodeNameResponse(ResponseRequestSchema):
    code: Optional[str] = Field(..., description="Mã")
    name: Optional[str] = Field(..., description="Tên")


class TransferTypeResponse(ResponseRequestSchema):
    receiving_method_type: Optional[str] = Field(..., description="Loại")
    receiving_method: Optional[str] = Field(
        ..., description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}"
    )


class ReceiverResponse(ResponseRequestSchema):
    account_number: Optional[str] = Field(None, description="Số tài khoản")
    fullname_vn: Optional[str] = Field(None, description="Chủ tài khoản")
    bank: DropdownCodeNameResponse = Field(None, description="Ngân hàng")
    bank_branch: Optional[str] = Field(None, description="Chi nhánh ngân hàng")
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
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    place_of_issue: Optional[DropdownResponse] = Field(..., description="Nơi cấp")


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


class CasaTopUpResponse(ResponseRequestSchema):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: FeeInfoResponse = Field(..., description="Thông tin phí")
    statement: StatementResponse = Field(..., description="Thông tin bảng kê")
    sender: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
