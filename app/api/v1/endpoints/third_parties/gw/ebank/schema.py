from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class CifInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF")


class GWRetrieveEbankByCIFNumberRequest(BaseSchema):
    cif_info: CifInfoRequest = Field(..., description="Dữ liệu đầu vào")


class EbankInfoItemResponse(BaseSchema):
    ebank_name: str = Field(..., description="Tên dịch vụ ebank")
    ebank_status: str = Field(..., description="Trạng thái dịch vụ ebank")


class GWRetrieveEbankByCIFNumberResponse(BaseSchema):
    ebank_info_item: EbankInfoItemResponse = Field(..., description="Thông tin Ebank")


class EbankIbmbInfoRequest(BaseSchema):
    ebank_ibmb_username: str = Field(..., description="Tên đăng nhập Internet Banking")
    ebank_ibmb_mobilephone: str = Field(..., description="Số điện thoại nhận OTP, 0933444938,...")


class CifOpenIbInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số Cif")


class AddressInfoRequest(BaseSchema):
    line: str = Field(..., description="Số nhà + tên đường")
    ward_name: str = Field(..., description="Tên Xã Phường")
    district_name: str = Field(..., description="Tên Quận Huyện")
    city_name: str = Field(..., description="Tên Tỉnh Thành")
    city_code: str = Field(..., description="Mã Tỉnh Thành")


class CustomerInfoRequest(BaseSchema):
    full_name: str = Field(..., description="Họ tên đầy đủ khách hàng")
    first_name: str = Field(..., description="Tên")
    middle_name: str = Field(..., description="Tên lót")
    last_name: str = Field(..., description="Họ")
    birthday: date = Field(..., description="Ngày sinh")
    email: str = Field(..., description="Email khách hàng")


class AuthenticationInfoRequest(BaseSchema):
    authentication_code: str = Field(..., description="Mảng mã loại hình xác thực. VD: [OTP, S_TOKEN]."
                                                      "Hiện loại hình xác thực chỉ có 2 loại OTP, S_TOKEN")


class ServicePackageInfoRequest(BaseSchema):
    service_package_code: str = Field(..., description="Mã gói hạn mức giao dịch Internet Banking")


class StaffRefererRequest(BaseSchema):
    staff_code: str = Field(..., description="Mã người giới thiệu")


class GWOpenIbRequest(BaseSchema):
    ebank_ibmb_info: EbankIbmbInfoRequest = Field(..., description="Thông tin Ebank")
    cif_info: CifOpenIbInfoRequest = Field(..., description="Thông tin Cif")
    address_info: AddressInfoRequest = Field(..., description="Thông tin địa chỉ")
    customer_info: CustomerInfoRequest = Field(..., description="Thông tin khách hàng")
    authentication_info: List[AuthenticationInfoRequest] = Field(..., description="Thông tin xác thực")
    service_package_info: ServicePackageInfoRequest = Field(..., description="Thông tin gói hạn mức giao dịch")
    staff_referer: StaffRefererRequest = Field(..., description="Thông tin người giới thiệu")
