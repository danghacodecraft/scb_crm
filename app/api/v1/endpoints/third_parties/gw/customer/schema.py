from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseGWSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import OptionalDropdownResponse


class CustomerInfoCIFResponse(BaseGWSchema):
    cif_number: str = CustomField().CIFNumberField


class CustomerInfoListCIFRequest(BaseGWSchema):
    cif_number: Optional[str] = Field("", description="Số CIF")
    identity_number: Optional[str] = Field("", description="Số CMND/CCCD/HC")
    mobile_number: Optional[str] = Field("", description="Số điện thoại")
    full_name: Optional[str] = Field("", description="Họ tên")


class GWCustomerCheckExistResponse(BaseGWSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCustomerCheckExistRequest(BaseGWSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerCIFInfoResponse(BaseGWSchema):
    customer_id: Optional[str] = Field(None, description="Mã khách hàng")
    cif_number: Optional[str] = Field(..., description="Số CIF")
    issued_date: Optional[str] = Field(..., description="Ngày cấp số CIF")


class GWCustomerIDInfoResponse(BaseGWSchema):
    number: Optional[str] = Field(
        ..., description="CMND/Hộ chiếu, số đăng ký kinh doanh nếu là khách hàng doanh nghiệp"
    )
    name: Optional[str] = Field(..., description="Tên giấy tờ")
    issued_date: Optional[date] = Field(..., description="Ngày cấp chứng minh nhân dân hoặc hộ chiếu")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn chứng minh nhân dân hoặc hộ chiếu")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp chứng minh nhân dân hoặc hộ chiếu")


class GWCustomerListAddressInfo(BaseGWSchema):
    address_full: Optional[str] = Field(..., description="Địa chỉ đầy đủ")


class GWCustomerListAddress(BaseGWSchema):
    contact_address_full: Optional[str] = Field(..., description="Địa chỉ liên lạc đầy đủ")
    address_full: Optional[str] = Field(..., description="Địa chỉ đầy đủ")


class GWCustomerDetailAddressInfo(BaseGWSchema):
    address_full: Optional[str] = Field(..., description="Địa chỉ đầy đủ")
    number_and_street: Optional[str] = Field(..., description="Địa chỉ liên lạc - tên đường, số nhà")
    ward: OptionalDropdownResponse = Field(..., description="Tên Địa chỉ liên lạc - phường/xã")
    district: OptionalDropdownResponse = Field(..., description="Tên Địa chỉ liên lạc - quận/huyện")
    province: OptionalDropdownResponse = Field(..., description="Tên Địa chỉ liên lạc - tỉnh/thành")


class GWCustomerInfoItemResponse(BaseGWSchema):
    fullname_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    martial_status: OptionalDropdownResponse = Field(..., description="Tình trạng hôn nhân")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    nationality: OptionalDropdownResponse = Field(..., description="mã quốc tịch")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    telephone: Optional[str] = Field(..., description="Điện thoại bàn")
    otherphone: Optional[str] = Field(..., description="Số điện thoại khác")
    customer_type: OptionalDropdownResponse = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    branch_info: OptionalDropdownResponse = Field(..., description="Thông tin đơn vị")
    address_info: GWCustomerListAddressInfo = Field(..., description="Thông tin địa chỉ")


class GWCustomerInfoListResponse(BaseGWSchema):
    total_items: int = Field(..., description="Số lượng khách hàng")
    customer_info_list: List[GWCustomerInfoItemResponse] = Field(..., description="Danh sách khách hàng")


class GWCustomerJobInfo(BaseGWSchema):
    name: Optional[str] = Field(..., description="Tên nghề nghiệp")
    code: Optional[str] = Field(..., description="Mã nghề nghiệp")


class GWCustomerInfoDetailResponse(BaseGWSchema):
    fullname_vn: Optional[str] = Field(..., description="Họ và tên")
    short_name: Optional[str] = Field(..., description="Tên viết tắt")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    martial_status: OptionalDropdownResponse = Field(..., description="Tình trạng hôn nhân")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    nationality: OptionalDropdownResponse = Field(..., description="Mã quốc tịch")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    telephone: Optional[str] = Field(..., description="Điện thoại bàn")
    otherphone: Optional[str] = Field(..., description="Số điện thoại khác")
    customer_type: OptionalDropdownResponse = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")
    customer_category: OptionalDropdownResponse = Field(..., description="Nhóm khách hàng (I_11, I_12,...)")
    resident_status: OptionalDropdownResponse = Field(..., description="Tình trạng cư trú")
    legal_representativeprsn_name: Optional[str] = Field(
        ..., description="Tên người đại diện theo pháp luật (doanh nghiệp)"
    )
    legal_representativeprsn_id: Optional[str] = Field(
        ..., description="Số chứng minh thư người đại diện theo pháp luật (doanh nghiệp)"
    )
    biz_contact_person_phone_num: Optional[str] = Field(..., description="Số điện thoại người liên hệ (doanh nghiệp)")
    biz_line: Optional[str] = Field(..., description="Ngành nghề hoạt động chính (doanh nghiệp)")
    biz_license_issue_date: Optional[date] = Field(..., description="Ngày thành lập doanh nghiệp")
    is_staff: Optional[str] = Field(..., description="Y nếu là CBNV, N nếu ko phải")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    resident_address: GWCustomerDetailAddressInfo = Field(..., description="Thông tin địa chỉ thường trú")
    contact_address: GWCustomerDetailAddressInfo = Field(..., description="Thông tin địa chỉ liên hệ")
    job_info: OptionalDropdownResponse = Field(..., description="Thông tin việc làm")
    branch_info: OptionalDropdownResponse = Field(..., description="Thông tin đơn vị")
    avatar_url: Optional[str] = Field(..., description="URL hình ảnh đại diện của người dùng")


class GWCoOwnerResponse(BaseGWSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[str] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    nationality: OptionalDropdownResponse = Field(..., description="mã quốc tịch")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    customer_type: OptionalDropdownResponse = Field(..., description="Loại khách hàng")
    co_owner_relationship: OptionalDropdownResponse = Field(..., description="Mối quan hệ đồng sở hữu")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    address_info: GWCustomerListAddress = Field(..., description="Thông tin địa chỉ")


class GWCoOwnerListResponse(BaseGWSchema):
    total_items: int = Field(..., description="Số lượng khách hàng")
    co_owner_info_list: List[GWCoOwnerResponse] = Field(..., description="Danh sách khách hàng")


class GWAuthorizedResponse(BaseGWSchema):
    full_name_vn: Optional[str] = Field(..., description="Họ và tên")
    date_of_birth: Optional[str] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    nationality: OptionalDropdownResponse = Field(..., description="mã quốc tịch")
    mobile_phone: Optional[str] = Field(..., description="Điện thoại di động")
    customer_type: Optional[str] = Field(..., description="Loại khách hàng")
    coowner_relationship: Optional[str] = Field(..., description="Mối quan hệ đồng sở hữu")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    address_info: GWCustomerListAddress = Field(..., description="Thông tin địa chỉ")


class GWAuthorizedListResponse(BaseGWSchema):
    total_items: int = Field(..., description="Số lượng khách hàng")
    authorized_info_list: List[GWAuthorizedResponse] = Field(..., description="Danh sách khách hàng")


class GWOpenCIFResponse(BaseGWSchema):
    cif_id: str = Field(..., description="CIF_ID Customer")
    cif_number: str = Field(..., description="CIF_NUMBER Customer")


########################################################################################################################
# GW
########################################################################################################################
class GWCIFInformation(BaseGWSchema):
    cif_number: str = CustomField().CIFNumberField
    issued_date: Optional[date] = Field(..., description="Ngày cấp số CIF")
    customer_type: OptionalDropdownResponse = Field(..., description="Loại khách hàng")


class GWCustomerInformation(BaseGWSchema):
    full_name: Optional[str] = Field(..., description="Họ và tên không dấu")
    full_name_vn: Optional[str] = Field(..., description="Họ và tên có dấu")
    first_name: Optional[str] = Field(..., description="Họ có dấu")
    middle_name: Optional[str] = Field(..., description="Tên lót có dấu")
    last_name: Optional[str] = Field(..., description="Họ có dấu")
    date_of_birth: Optional[date] = Field(..., description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    nationality: OptionalDropdownResponse = Field(..., description="Quốc tịch")
    mobile: Optional[str] = Field(..., description="Số điện thoại di động")
    telephone: Optional[str] = Field(..., description="Số điện thoại bàn")
    email: Optional[str] = Field(..., description="Email")


class GWCustomerIdentityInformation(BaseGWSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class GWAddressInfo(BaseGWSchema):
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường")
    address_full: Optional[str] = Field(..., description="Địa chỉ đầy đủ")


class GWCustomerAddressInfoRes(BaseGWSchema):
    resident_address: GWAddressInfo = Field(..., description="Địa chỉ thường trú")
    contact_address: GWAddressInfo = Field(..., description="Địa chỉ liên lạc")


class GuardianOrCustomerRelationshipByCIFNumberResponse(BaseGWSchema):
    cif_information: GWCIFInformation = Field(..., description="Thông tin CIF")
    customer_information: GWCustomerInformation = Field(..., description="Thông tin khách hàng")
    identity_information: GWCustomerIdentityInformation = Field(
        ...,
        description="Thông tin giấy tờ định danh khách hàng"
    )
    address_info: GWCustomerAddressInfoRes = Field(..., description="Thông tin địa chỉ khách hàng")
    avatar_url: Optional[str] = Field(..., description="URL hình ảnh đại diện của người dùng")


class NameOnCardResponse(BaseGWSchema):
    last_name_on_card: Optional[str] = Field(..., description="Tên")
    middle_name_on_card: Optional[str] = Field(..., description="tên lót")
    first_name_on_card: Optional[str] = Field(..., description="Họ")


class CardDeliveryAddressResponse(BaseGWSchema):
    branch: OptionalDropdownResponse = Field(..., description=" chi nhánh scb nhận thẻ")
    delivery_address: Optional[GWAddressInfo] = Field(..., descripion="Địa chỉ nhân thẻ")


class DebitCardByCIFNumberResponse(BaseGWSchema):
    cif_number: str = Field(..., description="Số CIF")
    name_on_card: NameOnCardResponse = Field(..., description="Tên trên thẻ")
    card_delivery_address: CardDeliveryAddressResponse = Field(..., description="Địa chỉ giao nhận thẻ")
    avatar_url: Optional[str] = Field(..., description="URL hình ảnh đại diện của người dùng")
