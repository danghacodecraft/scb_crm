from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import Field, validator

from app.api.base.schema import (
    BaseSchema, CreatedUpdatedBaseModel, TMSCreatedUpdatedBaseModel,
    TMSResponseSchema
)
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
    sender_full_name_vn: Optional[str] = Field('', description="Người giao dịch")
    sender_identity_number: Optional[str] = Field('', description="Giấy tờ định danh")
    sender_issued_date: Optional[date] = Field('', description="Ngày cấp")
    sender_place_of_issue: Optional[DropdownRequest] = Field('', description="Nơi cấp")
    sender_address_full: Optional[str] = Field('', description="Địa chỉ")
    sender_mobile_number: Optional[str] = Field('', description="Số điện thoại", regex=REGEX_NUMBER_ONLY)
    receiving_method: str = Field('', description=f"Hình thức nhận: {make_description_from_dict(RECEIVING_METHODS)}")
    fee_info: Optional[OneFeeInfoRequest] = Field(..., description="Thông tin phí")
    fee_note: Optional[str] = Field('', description="Ghi chú phí")
    statement: List[StatementInfoRequest] = Field(..., description="Thông tin bảng kê")
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")
    amount: int = Field(..., description="Số tiền")
    content: str = Field(
        ..., description="Nội dung chuyển tiền", regex=REGEX_TRANSFER_CONTENT, max_length=MAX_LENGTH_TRANSFER_CONTENT
    )
    p_instrument_number: Optional[str] = Field('', description="Số bút toán")
    core_fcc_request: Optional[str] = Field('', description="")

    @validator("sender_mobile_number")
    def check_valid_mobile_number(cls, v):
        if v != '':
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
    receiver_mobile_number: Optional[str] = Field('', description="Số điện thoại")

    @validator("receiver_mobile_number")
    def check_valid_mobile_number(cls, v):
        if v != '':
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
    account_number: Optional[str] = Field('', description="Số tài khoản")
    card_number: Optional[str] = Field('', description="Số thẻ")
    fullname_vn: Optional[str] = Field('', description="Chủ tài khoản")
    bank: DropdownCodeNameResponse = Field('', description="Ngân hàng")
    bank_branch: Optional[str] = Field('', description="Chi nhánh ngân hàng")
    province: DropdownCodeNameResponse = Field('', description="Tỉnh/Thành phố")
    branch_info: DropdownCodeNameResponse = Field('', description="Đơn vị thụ hưởng")
    identity_number: Optional[str] = Field('', description="Số giấy tờ định danh")
    issued_date: Optional[date] = Field('', description="Ngày cấp")
    place_of_issue: DropdownCodeNameResponse = Field('', description="Nơi cấp")
    mobile_number: Optional[str] = Field('', description="Số điện thoại")
    address_full: Optional[str] = Field('', description="Địa chỉ")
    currency: Optional[str] = Field('', description="Loại tiền")


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
    payer: Optional[str] = Field('', description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field('', description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field('', description="Mã loại phí")
    amount: int = Field('', description='Số tiền phí')
    vat: int = Field('', description='Thuế VAT')
    total: int = Field('', description='Tổng phí')
    actual_total: Optional[float] = Field('', description="Số tiền thực chuyển")
    note: str = Field('', description='Nội dung')
    ref_num: str = Field('', description='Số bút toán')


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
    payer: Optional[str] = Field('', description="Bên thanh toán phí")
    fee_category: Optional[DropdownResponse] = Field('', description="Nhóm phí")
    fee: Optional[DropdownResponse] = Field('', description="Mã loại phí")
    vat: Optional[str] = Field('', description='Thuế VAT')
    total: Optional[str] = Field('', description='Tổng phí')
    actual_total: Optional[str] = Field('', description="Số tiền thực chuyển")
    note: Optional[str] = Field('', description='Nội dung')
    ref_num: Optional[str] = Field('', description='Số bút toán')


class TMSCasaTopUpResponse(TMSCreatedUpdatedBaseModel):
    transfer_type: TransferTypeResponse = Field(..., description="Loại chuyển")
    receiver: ReceiverResponse = Field(..., description="Thông tin người thụ hưởng")
    transfer: TransferResponse = Field(..., description="Thông tin giao dịch")
    fee_info: Optional[FeeDetailInfoResponse] = Field(..., description="Thông tin phí")
    statement: TMSStatementResponse = Field(..., description="Thông tin bảng kê")
    sender: CustomerResponse = Field(..., description="Thông tin khách hàng giao dịch")
    direct_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")
    indirect_staff: StaffInfoResponse = Field(..., description="Thông tin khách hàng giao dịch")


class TemplateFieldWarning(BaseSchema):
    id: int = Field(..., description="id template field ")
    key: str = Field(..., description="key tempalte field")
    label: str = Field(..., description="nhãn template field")
    error_description: str = Field(..., description="Mô tả lỗi")


class TemplateGroupWaring(BaseSchema):
    group_id: int = Field(..., description="id group")
    group_name: str = Field(..., description="Tên group")
    error_description: str = Field(..., description="Mô tả lỗi")


class TMSFillDatResponse(BaseSchema):
    file_url: str = Field(..., description="đường đẫn file từ Minio")
    created_at: datetime = Field(..., description="thời gian fill data vào biểu mẫu")
    is_warning: bool = Field(..., description='Có cảnh báo `False`: Không có cảnh báo, <br> `True`: Có cảnh báo')
    template_field_warnings: List[TemplateFieldWarning] = Field(...)
    group_warning: List[TemplateGroupWaring] = Field(...)
    fill_data_version_id: int = Field(..., description="Id phiên bản nhập liệu")
    fill_data_history_id: int = Field(..., description="Id lịch sử nhập liêu")
    file_uuid: str = Field(..., description="file uuid sau khi đổ dữ liệu")


class TMSTemplateInfoResponse(BaseSchema):
    template_id: int = Field(..., description='id template')
    template_name: str = Field(..., description="Tên template")
    template_fill_data_info: TMSFillDatResponse = Field(...)


class TMSApprovalResponse(CreatedUpdatedBaseModel):
    folder_name: str = Field(..., description='Tên folder')
    templates: List[TMSTemplateInfoResponse] = Field(...)
