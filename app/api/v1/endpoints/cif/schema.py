from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownResponse, OptionalDropdownResponse
from app.utils.constant.gw import (
    GW_REQUEST_PARAMETER, GW_REQUEST_PARAMETER_DEFAULT
)


class CifInformationResponse(BaseSchema):
    self_selected_cif_flag: bool = Field(..., description='Cờ CIF thông thường/ tự chọn. '
                                                          '`False`: thông thường. '
                                                          '`True`: tự chọn')
    cif_number: Optional[str] = CustomField(description='Số CIF yêu cầu').OptionalCIFNumberField
    customer_classification: DropdownResponse = Field(..., description='Đối tượng khách hàng')
    customer_economic_profession: DropdownResponse = Field(..., description='Mã ngành KT')
    kyc_level: DropdownResponse = Field(..., description='Cấp độ KYC')


class CheckExistCIFSuccessResponse(BaseSchema):
    is_existed: bool = Field(...,
                             description="Cờ đã tồn tại hay chưa <br>`True` => tồn tại <br>`False` => chưa tồn tại")


class CheckExistCIFRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


# ################################### lịch sử hồ sơ (log)####################################3
class ProfileHistoryOfDayResponse(BaseSchema):
    description: str = Field(..., description="Mô tả")
    completed_at: datetime = Field(..., description="Thời gian hoàn thành")
    started_at: datetime = Field(..., description="Thời gian bắt đầu hoàn thành")
    status: str = Field(..., description="Trạng thái hồ sơ")
    branch_id: str = Field(..., description="ID chi nhánh")
    branch_code: str = Field(..., description="Mã chi nhánh")
    branch_name: str = Field(..., description="Tên chi nhánh")
    user_id: str = Field(..., description="ID nhân viên")
    user_name: str = Field(..., description="Tên nhân viên")
    position_id: str = Field(..., description="ID Chức vụ")
    position_code: str = Field(..., description="Mã Chức vụ")
    position_name: str = Field(..., description="Tên Chức vụ")


class CifProfileHistoryResponse(BaseSchema):
    created_at: date = Field(..., description="Ngày tạo hồ sơ")
    log_details: List[ProfileHistoryOfDayResponse] = Field(..., description="Danh sách log trong 1 ngày")


################################################################
# Thông tin khách hàng (Customer)
################################################################

class StatusResponse(DropdownResponse):
    active_flag: bool = Field(..., description="Cờ đóng mở. `False`: Đóng. `True`: Mở")


class EmployeeResponse(BaseSchema):
    id: str = Field(..., description="Mã định danh")
    full_name_vn: Optional[str] = Field(..., description="Tên tiếng việt")
    avatar_url: Optional[str] = Field(..., description="Đường dẫn hình ảnh")
    user_name: Optional[str] = Field(..., description="Tên")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    avatar: Optional[str] = Field(..., description="Avatar")
    position: OptionalDropdownResponse = Field(..., description="Chức danh")
    department: OptionalDropdownResponse = Field(..., description="Phòng")
    branch: OptionalDropdownResponse = Field(..., description="Đơn vị")
    title: OptionalDropdownResponse = Field(..., description="Đơn vị")


class CifCustomerInformationResponse(BaseSchema):
    customer_id: str = Field(..., description="Mã định danh khách hàng")
    status: StatusResponse = Field(..., description="Trạng thái")
    cif_number: Optional[str] = CustomField().OptionalCIFNumberField
    avatar_url: Optional[str] = Field(..., description="Đường dẫn hình ảnh khách hàng")
    customer_classification: DropdownResponse = Field(..., description="Hạng khách hàng")
    full_name: str = Field(..., description="Họ tên tiếng anh")
    gender: DropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Địa chỉ email")
    mobile_number: Optional[str] = Field(..., description="Số điện thoại")
    identity_number: str = Field(..., description="Số giấy tờ định danh")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    date_of_birth: date = Field(..., description="Ngày sinh")
    nationality: DropdownResponse = Field(..., description="Quốc tịch")
    marital_status: OptionalDropdownResponse = Field(..., description="Tình trạng hôn nhân")
    # TODO: thông tin về loại khách hàng khi tạo CIF chưa có
    customer_type: OptionalDropdownResponse = Field(None, description="Loại khách hàng")
    # TODO: hạng tín dụng chưa có field trong customer
    credit_rating: Optional[str] = Field(..., description="Hạng tín dng")
    address: str = Field(..., description="Địa chỉ")
    total_employees: int = Field(..., description="Tổng số người tham gia")
    employees: List[EmployeeResponse] = Field(..., description="Danh sách nhân viên")


class SOACIFInformation(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    issued_date: str = Field(None, description="Ngày cấp số CIF")
    branch_code: str = Field(None, description="Mã chi nhánh")
    customer_type: str = Field(None, description="Loại khách hàng")


class SOACustomerInformation(BaseSchema):
    full_name: Optional[str] = Field(None, description="Họ và tên không dấu")
    full_name_vn: Optional[str] = Field(None, description="Họ và tên có dấu")
    first_name: Optional[str] = Field(None, description="Họ có dấu")
    middle_name: Optional[str] = Field(None, description="Tên lót có dấu")
    last_name: Optional[str] = Field(None, description="Họ có dấu")
    date_of_birth: Optional[str] = Field(None, description="Ngày sinh")
    gender: OptionalDropdownResponse = Field(..., description="Giới tính")
    customer_vip_type: Optional[str] = Field(None, description="Loại VIP khách hàng")
    manage_staff_id: Optional[str] = Field(None, description="Mã nhân viên quản lý")
    director_name: Optional[str] = Field(None, description="Người đại diện( khách hàng doanh nghiệp)")
    nationality_code: Optional[str] = Field(None, description="Mã quốc tịch")
    nationality: Optional[str] = Field(None, description="Quốc tịch")
    is_staff: Optional[str] = Field(None, description="Có phải nhân viên ngân hàng")
    segment_type: Optional[str] = Field(None, description="Segment khách hàng")


class SOACustomerIdentityInformation(BaseSchema):
    identity_number: Optional[str] = Field(None, description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    # place_of_issue: OptionalDropdownResponse = Field(None, description="Nơi cấp")


class SOAAddressInfo(BaseSchema):
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    name: Optional[str] = Field(..., description="Địa chỉ")


class SOACustomerAddressInfoRes(BaseSchema):
    resident_address: SOAAddressInfo = Field(..., description="Địa chỉ thường trú")
    contact_address: SOAAddressInfo = Field(..., description="Địa chỉ liên lạc")
    email: Optional[str] = Field(None, description="Email")
    mobileNum: Optional[str] = Field(None, description="Mobile Number")
    telephoneNum: Optional[str] = Field(None, description="Telephone Number")
    phoneNum: Optional[str] = Field(None, description="Phone Number")
    faxNum: Optional[str] = Field(None, description="Số fax")


########################################################################################################################
# GW
########################################################################################################################
class GWCIFInformation(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    issued_date: Optional[str] = Field(..., description="Ngày cấp số CIF")
    customer_type: OptionalDropdownResponse = Field(..., description="Loại khách hàng")


class GWCustomerInformation(BaseSchema):
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


class GWCustomerIdentityInformation(BaseSchema):
    identity_number: Optional[str] = Field(..., description="Số CMND/CCCD/Hộ chiếu")
    issued_date: Optional[date] = Field(..., description="Ngày cấp")
    expired_date: Optional[date] = Field(..., description="Ngày hết hạn")
    place_of_issue: OptionalDropdownResponse = Field(..., description="Nơi cấp")


class GWAddressInfo(BaseSchema):
    province: OptionalDropdownResponse = Field(..., description="Tỉnh/Thành phố")
    district: OptionalDropdownResponse = Field(..., description="Quận/Huyện")
    ward: OptionalDropdownResponse = Field(..., description="Phường/Xã")
    number_and_street: Optional[str] = Field(..., description="Số nhà, tên đường")
    address_full: Optional[str] = Field(..., description="Địa chỉ đầy đủ")


class GWCustomerAddressInfoRes(BaseSchema):
    resident_address: GWAddressInfo = Field(..., description="Địa chỉ thường trú")
    contact_address: GWAddressInfo = Field(..., description="Địa chỉ liên lạc")


class CustomerByCIFNumberResponse(BaseSchema):
    cif_information: GWCIFInformation = Field(..., description="Thông tin CIF")
    customer_information: GWCustomerInformation = Field(..., description="Thông tin khách hàng")
    identity_information: GWCustomerIdentityInformation = Field(
        ...,
        description="Thông tin giấy tờ định danh khách hàng"
    )
    address_info: GWCustomerAddressInfoRes = Field(..., description="Thông tin địa chỉ khách hàng")
    # cif_information: SOACIFInformation = Field(..., description="Thông tin CIF")
    # customer_information: SOACustomerInformation = Field(..., description="Thông tin khách hàng")
    # # career_information: DropdownResponse = Field(..., description="Thông tin nghề nghiệp khách hàng")
    # identity_information: SOACustomerIdentityInformation = Field(...,
    #                                                              description="Thông tin giấy tờ định danh khách hàng")
    # address_info: SOACustomerAddressInfoRes = Field(..., description="Thông tin địa chỉ khách hàng")


class CustomerByCIFNumberRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerDetailRequest(BaseSchema):
    parameter: str = Field(GW_REQUEST_PARAMETER_DEFAULT, description=f"""Tham số truyền vào `{GW_REQUEST_PARAMETER}`""")
