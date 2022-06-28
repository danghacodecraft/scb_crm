from datetime import date
from typing import Optional, List

from pydantic import Field

from app.api.base.schema import RequestSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest
from app.utils.regex import REGEX_NUMBER_ONLY, REGEX_TRANSFER_CONTENT, MAX_LENGTH_TRANSFER_CONTENT


class FeeInfoRequest(RequestSchema):
    payer: str = Field(..., description="Bên thanh toán phí")
    fee_amount: str = Field(..., description="Số tiền phí")
    note: Optional[str] = Field(..., description="Ghi chú")


class StatementInfoRequest(RequestSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: str = Field(..., description="Số lượng", regex=REGEX_NUMBER_ONLY)


# Common
class PayInCashRequest(RequestSchema):
    cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    receiving_method: str = Field(..., description="Hình thức nhận")
    is_fee: bool = Field(..., description="Có thu phí không")
    fee_info: Optional[FeeInfoRequest] = Field(..., description="Thông tin phí")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    direct_staff: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")


########################################################################################################################
# Thông tin người thụ hưởng
########################################################################################################################
class PayInCashSCBToAccountRequest(PayInCashRequest):
    """
    Trong SCB đến tài khoản
    """
    account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    amount: str = Field(..., description="Số tiền", regex=REGEX_NUMBER_ONLY)
    content: Optional[str] = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )


class PayInCashSCBByIdentity(PayInCashRequest):
    """
        Trong SCB nhận bằng giấy tờ định danh
    """
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    branch: DropdownRequest = Field(..., description="Đơn vị thụ hưởng")
    full_name_vn: str = Field(..., description="Họ tên người thụ hưởng")
    identity_number: str = Field(..., description="Số GTĐD", regex=REGEX_NUMBER_ONLY)
    issued_date: date = Field(..., description="Ngày cấp")
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")
    mobile_number: Optional[str] = Field(..., description="Số điện thoại")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)
    amount: str = Field(..., description="Số tiền", regex=REGEX_NUMBER_ONLY)
    content: str = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )


class PayInCashThirdPartyToAccount(PayInCashRequest):
    """
    Ngoài SCB đến tài khoản
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    province: DropdownRequest = Field(..., description="Tỉnh/Thành phố")
    branch: DropdownRequest = Field(..., description="Chi nhánh")
    full_name_vn: str = Field(..., description="Chủ tài khoản")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


class PayInCashThirdPartyByIdentity(PayInCashRequest):
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


class PayInCashThirdParty247ToAccount(PayInCashRequest):
    """
    Ngoài SCB 24/7 tài khoản
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    account_number: str = Field(..., description="Số tài khoản", regex=REGEX_NUMBER_ONLY)
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


class PayInCashThirdParty247ToCard(PayInCashRequest):
    """
    Ngoài SCB 24/7 số thẻ
    """
    bank: DropdownRequest = Field(..., description="Ngân hàng")
    card_number: str = Field(..., description="Số thẻ")
    address_full: str = Field(..., description="Địa chỉ", max_length=100)


########################################################################################################################


class PayInCashResponse(RequestSchema):
    pass
