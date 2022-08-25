from datetime import date
from typing import List, Optional, Union

from pydantic import Field, validator

from app.api.base.schema import CreatedUpdatedBaseModel, TMSResponseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.others.fee.schema import OneFeeInfoRequest
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownResponse
)
from app.utils.constant.casa import RECEIVING_METHODS
from app.utils.functions import (
    is_valid_mobile_number, make_description_from_dict
)
from app.utils.regex import (
    MAX_LENGTH_TRANSFER_CONTENT, REGEX_NUMBER_ONLY, REGEX_TRANSFER_CONTENT
)


class StatementInfoRequest(TMSResponseSchema):
    denominations: str = Field(..., description="Mệnh giá")
    amount: int = Field(..., description="Số lượng")


# Common
class CasaTopUpCommonRequest(TMSResponseSchema):
    sender_cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    sender_full_name_vn: Optional[str] = Field(None, description="Người giao dịch")
    sender_identity_number: Optional[str] = Field(None, description="Giấy tờ định danh")
    sender_issued_date: Optional[date] = Field(None, description="Ngày cấp")
    sender_place_of_issue: Optional[DropdownRequest] = Field(None, description="Nơi cấp")
    sender_address_full: Optional[str] = Field(None, description="Địa chỉ")
    sender_mobile_number: Optional[str] = Field(None, description="Số điện thoại", regex=REGEX_NUMBER_ONLY)
    receiving_method: str = Field(None, description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}")
    fee_info: Optional[OneFeeInfoRequest] = Field(..., description="Thông tin phí")
    fee_note: Optional[str] = Field(None, description="Ghi chú phí")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")
    amount: int = Field(..., description="Số tiền")
    content: str = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )
    p_instrument_number: Optional[str] = Field(None, description="Số bút toán")
    core_fcc_request: Optional[str] = Field(None, description="")

    @validator("sender_mobile_number")
    def check_valid_mobile_number(cls, v):
        if v is not None:
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
        if v is not None:
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


class CasaTopUpRequest(TMSResponseSchema):
    customer_cif_number: str = CustomField().CIFNumberField
    receiving_method: str = Field(..., description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}")
    data: Union[
        CasaTopUpSCBByIdentityRequest,
        CasaTopUpThirdPartyByIdentityRequest,
        CasaTopUpThirdPartyToAccountRequest,
        CasaTopUpThirdParty247ToAccountRequest,
        CasaTopUpSCBToAccountRequest,
        CasaTopUpThirdParty247ToCardRequest
    ] = Field(..., description="Nội dung")


########################################################################################################################
class DropdownCodeNameResponse(TMSResponseSchema):
    code: Optional[str] = Field(..., description="Mã")
    name: Optional[str] = Field(..., description="Tên")


class TransferTypeResponse(TMSResponseSchema):
    receiving_method_type: Optional[str] = Field(..., description="Loại")
    receiving_method: Optional[str] = Field(
        ..., description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}"
    )


class ReceiverResponse(TMSResponseSchema):
    account_number: Optional[str] = Field(None, description="Số tài khoản")
    card_number: Optional[str] = Field(None, description="Số thẻ")
    fullname_vn: Optional[str] = Field(None, description="Chủ tài khoản")
    bank: DropdownCodeNameResponse = Field(None, description="Ngân hàng")
    bank_branch: Optional[str] = Field(None, description="Chi nhánh ngân hàng")
    province: DropdownCodeNameResponse = Field(None, description="Tỉnh/Thành phố")
    branch_info: DropdownCodeNameResponse = Field(None, description="Đơn vị thụ hưởng")
    identity_number: Optional[str] = Field(None, description="Số giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: DropdownCodeNameResponse = Field(None, description="Nơi cấp")
    mobile_number: Optional[str] = Field(None, description="Số điện thoại")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    currency: Optional[str] = Field(None, description="Loại tiền")


class TransferResponse(TMSResponseSchema):
    amount: int = Field(..., description="Số tiền")
    content: str = Field(..., description="Nội dung chuyển tiền")
    entry_number: Optional[str] = Field(..., description="Số bút toán")


class IdentityInfoResponse(TMSResponseSchema):
    number: Optional[str] = Field(..., description="Số GTDD")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class CustomerResponse(TMSResponseSchema):
    cif_number: Optional[str] = Field(..., description="Số CIF")
    fullname_vn: Optional[str] = Field(..., description="Người giao dịch")
    address_full: Optional[str] = Field(..., description="Địa chỉ")
    identity_info: IdentityInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    mobile_phone: Optional[str] = Field(..., description="SĐT")
    telephone: Optional[str] = Field(..., description="SĐT")
    otherphone: Optional[str] = Field(..., description="SĐT")


class StaffInfoResponse(TMSResponseSchema):
    code: Optional[str] = Field(..., description="Mã NV")
    name: Optional[str] = Field(..., description="Tên NV")


class TMSFeeDetailInfoResponse(TMSResponseSchema):
    payer: Optional[str] = Field(None, description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field(None, description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field(None, description="Mã loại phí")
    amount: int = Field(None, description='Số tiền phí')
    vat: int = Field(None, description='Thuế VAT')
    total: int = Field(None, description='Tổng phí')
    actual_total: Optional[float] = Field(None, description="Số tiền thực chuyển")
    note: str = Field(None, description='Nội dung')
    ref_num: str = Field(None, description='Số bút toán')


class StatementsResponse(TMSResponseSchema):
    denominations: Optional[str] = Field(..., description="Mệnh giá")
    amount: str = Field(..., description="Số lượng")
    into_money: str = Field(..., description="Thành tiền")


class TMSStatementResponse(TMSResponseSchema):
    statements: List[StatementsResponse] = Field(..., description="Thông tin chi tiết bảng kê")
    total: str = Field(..., description="Tổng thành tiền")
    odd_difference: str = Field(..., description="Chênh lệch lẻ")
    total_number_of_bills: Optional[str] = Field('0', description="tổng số lượng bill")


class FeeDetailInfoResponse(TMSResponseSchema):
    payer: Optional[str] = Field(None, description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field(None, description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field(None, description="Mã loại phí")
    amount: int = Field(None, description='Số tiền phí')
    vat: int = Field(None, description='Thuế VAT')
    total: int = Field(None, description='Tổng phí')
    actual_total: Optional[float] = Field(None, description="Số tiền thực chuyển")
    note: str = Field(None, description='Nội dung')
    ref_num: str = Field(None, description='Số bút toán')


class TMSCasaTopUpResponse(CreatedUpdatedBaseModel):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: Optional[FeeDetailInfoResponse] = Field(..., description="Thông tin phí")
    statement: TMSStatementResponse = Field(..., description="Thông tin bảng kê")
    sender: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
