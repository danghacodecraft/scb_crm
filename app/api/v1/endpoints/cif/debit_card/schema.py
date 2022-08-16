from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.cif import AddressRequest, OptionalAddressResponse
from app.api.v1.schemas.utils import (
    DropdownRequest, DropdownResponse, OptionalDropdownResponse
)


class NameOnCardResponse(BaseSchema):
    last_name_on_card: str = Field(..., description="Tên")
    middle_name_on_card: str = Field(None, description="tên lót")
    first_name_on_card: str = Field(..., description="Họ")


class MainAndSubCardNumberResponse(BaseSchema):
    number_part_1: str = Field(..., description="4 số đầu trên thẻ")
    number_part_2: str = Field(..., description="4 số thứ 2 trên thẻ")
    number_part_3: str = Field(..., description="4 số thứ 3 trên thẻ")
    number_part_4: str = Field(..., description="4 số cuối trên thẻ")


class IssueDebitCardResponse(BaseSchema):
    register_flag: bool = Field(..., description="Đăng kí thẻ ghi nợ, `True`: đăng kí, `False`: không đăng kí ")
    physical_card_type: List[DropdownResponse] = Field(..., description="TÍnh vật lý: thẻ vật lý, thẻ phi vật lý",
                                                       nullable=True)
    physical_issuance_type: DropdownResponse = Field(None, description="Hình thức phát hành")
    customer_type: DropdownResponse = Field(None, description="Nhóm khách hàng")
    payment_online_flag: bool = Field(None, description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    branch_of_card: DropdownResponse = Field(None, description="Thương hiệu thẻ")
    issuance_fee: DropdownResponse = Field(None, description="Phí phat hành thẻ")
    annual_fee: DropdownResponse = Field(None, description="Phí thường niên")
    src_code: str = Field(..., description="Mã source")
    pro_code: str = Field(..., description="Mã promo")


class InformationDebitCardResponse(BaseSchema):
    name_on_card: NameOnCardResponse = Field(None, description="Tên trên thẻ")
    main_card_number: MainAndSubCardNumberResponse = Field(None, description="Số thẻ chính")
    card_image_url: str = Field(None, description="Url hình ảnh thẻ")


class CardDeliveryAddressResponse(BaseSchema):
    delivery_address_flag: bool = Field(..., description="Địa chỉ nhận tại SCB. "
                                                         "`Fasle`: tại SCB, "
                                                         "`True`:địa chỉ khác")
    scb_branch: Optional[DropdownResponse] = Field(None, description=" chi nhánh scb nhận thẻ")
    delivery_address: Optional[OptionalAddressResponse] = Field(None, descripion="Địa chỉ nhân thẻ")
    note: Optional[str] = Field(None, description="ghi chú")


class SubDebitCardResponse(BaseSchema):
    id: str = Field(..., description="Id thẻ phụ")
    cif_number: str = CustomField().CIFNumberField
    name_on_card: NameOnCardResponse = Field(..., description="Tên trên thẻ")
    physical_card_type: List[DropdownResponse] = Field(..., description="TÍnh vật lý: thẻ vật lý, thẻ phi vật lý")
    card_issuance_type: DropdownResponse = Field(..., description="Hình thức phát hành")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    card_delivery_address: CardDeliveryAddressResponse = Field(None, description="Địa chỉ giao nhận thẻ")
    card_image_url: str = Field(..., description="Url hình ảnh thẻ ")


class InformationSubDebitCardResponse(BaseSchema):
    sub_debit_cards: List[SubDebitCardResponse] = Field(None, description="Danh sách thẻ phụ ")
    total_sub_debit_card: int = Field(..., description="Tổng số thẻ phụ ")


class DebitCardResponse(BaseSchema):
    issue_debit_card: IssueDebitCardResponse = Field(None, description="Phát hành thẻ ghi nợ ")
    information_debit_card: InformationDebitCardResponse = Field(None, description="Thông tin thẻ ")
    card_delivery_address: CardDeliveryAddressResponse = Field(None, description="Địa chỉ nhân thẻ ")
    information_sub_debit_card: InformationSubDebitCardResponse = Field(None, description="Thông tin thẻ phụ")
    booking: OptionalDropdownResponse = Field(..., description="Booking")


# ######################### request schema ###################################
class NameOnCardRequest(BaseSchema):
    last_name_on_card: str = Field(..., description="Tên")
    middle_name_on_card: str = Field(None, description="tên lót")
    first_name_on_card: str = Field(..., description="Họ")


class IssueDebitRequest(BaseSchema):
    register_flag: bool = Field(..., description="Đăng kí thẻ ghi nợ, `True`: đăng kí, `False`: không đăng kí ")
    physical_card_type: List[DropdownRequest] = Field(..., description="TÍnh vật lý")
    physical_issuance_type: DropdownRequest = Field(..., description="Hình thức phát hành")
    customer_type: DropdownRequest = Field(..., description="Nhóm khách hàng")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    branch_of_card: DropdownRequest = Field(..., description="Thương hiệu thẻ")
    issuance_fee: DropdownRequest = Field(..., description="Phí phat hành thẻ")
    annual_fee: DropdownRequest = Field(..., description="Phí thường niên")
    src_code: str = Field(..., description="Mã source")
    pro_code: str = Field(..., description="Mã promo")


class CardDeliveryAddressRequest(BaseSchema):
    delivery_address_flag: bool = Field(..., description="Địa chỉ nhận tại SCB. "
                                                         "`Fasle`: tại SCB, "
                                                         "`True`:địa chỉ khác")
    scb_branch: Optional[DropdownRequest] = Field(None, description=" chi nhánh scb nhận thẻ")
    delivery_address: Optional[AddressRequest] = Field(None, descripion="Địa chỉ nhân thẻ")
    note: str = Field(None, description="ghi chú")


class SubDebitCardRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    name_on_card: NameOnCardRequest = Field(..., description="Tên trên thẻ")
    physical_card_type: List[DropdownRequest] = Field(..., description="TÍnh vật lý")
    card_issuance_type: DropdownRequest = Field(..., description="Hình thức phát hành")
    payment_online_flag: bool = Field(..., description="Mở chức năng thanh toán online, `True`: có, `False`: không")
    card_delivery_address: CardDeliveryAddressRequest = Field(..., description="Địa chỉ giao nhận thẻ")


class InformationSubDebitCardRequest(BaseSchema):
    sub_debit_cards: List[SubDebitCardRequest] = Field(..., description="Danh sách thẻ phụ ")


class InformationDebitCardRequest(BaseSchema):
    name_on_card: NameOnCardRequest = Field(..., description="Tên trên thẻ")


class DebitCardRequest(BaseSchema):
    issue_debit_card: IssueDebitRequest = Field(..., description="Phát hành thẻ ghi nợ ")
    information_debit_card: InformationDebitCardRequest = Field(..., description="Thông tin thẻ ")
    card_delivery_address: CardDeliveryAddressRequest = Field(..., description="Địa chỉ nhân thẻ ")
    information_sub_debit_card: Optional[InformationSubDebitCardRequest] = Field(None, description="Thông tin thẻ phụ")


class SubCusResponse(BaseSchema):
    first_name: str = Field(..., description="Họ")
    last_name: str = Field(..., description="Tên")
