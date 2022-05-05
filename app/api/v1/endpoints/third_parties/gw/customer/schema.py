from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.third_parties.gw.schema import (
    GWBranchDropdownResponse
)


class CustomerInfoCIFResponse(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class CustomerInfoListCIFRequest(BaseSchema):
    cif_number: str = Field("", description="Số CIF")
    identity_number: str = Field("", description="Số CMND/CCCD/HC")
    mobile_number: str = Field("", description="Số điện thoại")
    full_name: str = Field("", description="Họ tên")


class GWCustomerCheckExistResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCustomerCheckExistRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerCIFInfoResponse(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    issued_date: str = Field(..., description="Ngày cấp số CIF")


class GWCustomerIDInfoResponse(BaseSchema):
    number: str = Field(..., description="CMND/Hộ chiếu, số đăng ký kinh doanh nếu là khách hàng doanh nghiệp")
    name: str = Field(..., description="Tên giấy tờ")
    issued_date: str = Field(..., description="Ngày cấp chứng minh nhân dân hoặc hộ chiếu")
    expired_date: str = Field(..., description="Ngày hết hạn chứng minh nhân dân hoặc hộ chiếu")
    place_of_issue: str = Field(..., description="Nơi cấp chứng minh nhân dân hoặc hộ chiếu")


class GWCustomerListAddressInfo(BaseSchema):
    address_full: str = Field(..., description="Địa chỉ đầy đủ")


class GWCustomerDetailAddressInfo(BaseSchema):
    address_full: str = Field(..., description="Địa chỉ đầy đủ")
    contact_address_full: str = Field(..., description="Địa chỉ liên lạc đầy đủ")


class GWCustomerInfoItemResponse(BaseSchema):
    fullname_vn: str = Field(..., description="Họ và tên")
    date_of_birth: str = Field(..., description="Ngày sinh")
    martial_status: str = Field(..., description="Tình trạng hôn nhân")
    gender: str = Field(..., description="Giới tính")
    email: str = Field(..., description="Địa chỉ email")
    nationality_code: str = Field(..., description="mã quốc tịch")
    mobile_phone: str = Field(..., description="Điện thoại di động")
    telephone: str = Field(..., description="Điện thoại bàn")
    otherphone: str = Field(..., description="Số điện thoại khác")
    customer_type: str = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin đơn vị")
    address_info: GWCustomerListAddressInfo = Field(..., description="Thông tin địa chỉ")


class GWCustomerInfoListResponse(BaseSchema):
    total_items: int = Field(..., description="Số lượng khách hàng")
    customer_info_list: List[GWCustomerInfoItemResponse] = Field(..., description="Danh sách khách hàng")


class GWCustomerJobInfo(BaseSchema):
    name: str = Field(..., description="Tên nghề nghiệp")
    code: str = Field(..., description="Mã nghề nghiệp")


class GWCustomerInfoDetailResponse(BaseSchema):
    fullname_vn: str = Field(..., description="Họ và tên")
    short_name: str = Field(..., description="Tên viết tắt")
    date_of_birth: str = Field(..., description="Ngày sinh")
    martial_status: str = Field(..., description="Tình trạng hôn nhân")
    gender: str = Field(..., description="Giới tính")
    email: str = Field(..., description="Địa chỉ email")
    nationality_code: str = Field(..., description="Mã quốc tịch")
    mobile_phone: str = Field(..., description="Điện thoại di động")
    telephone: str = Field(..., description="Điện thoại bàn")
    otherphone: str = Field(..., description="Số điện thoại khác")
    customer_type: str = Field(..., description="Loại khách hàng (cá nhân hoặc doanh nghiệp)")
    resident_status: str = Field(..., description="Tình trạng cư trú")
    legal_representativeprsn_name: str = Field(..., description="Tên người đại diện theo pháp luật (doanh nghiệp)")
    legal_representativeprsn_id: str = Field(..., description="Số chứng minh thư người đại diện theo pháp luật (doanh nghiệp)")
    biz_contact_person_phone_num: str = Field(..., description="Số điện thoại người liên hệ (doanh nghiệp)")
    biz_line: str = Field(..., description="Ngành nghề hoạt động chính (doanh nghiệp)")
    biz_license_issue_date: str = Field(..., description="Ngày thành lập doanh nghiệp")
    is_staff: str = Field(..., description="Y nếu là CBNV, N nếu ko phải")
    cif_info: GWCustomerCIFInfoResponse = Field(..., description="Thông tin CIF")
    id_info: GWCustomerIDInfoResponse = Field(..., description="Thông tin giấy tờ định danh")
    address_info: GWCustomerDetailAddressInfo = Field(..., description="Thông tin địa chỉ")
    job_info: GWCustomerJobInfo = Field(..., description="Thông tin việc làm")
    branch_info: GWBranchDropdownResponse = Field(..., description="Thông tin đơn vị")
