from datetime import date, datetime
from typing import List, Union

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


class InternetBankingStaffInfo(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")


class InternetBankingServicePackInfo(BaseSchema):
    service_package_code: str = Field(..., description="Mã gói dịch vụ khi đăng ký IBMB")
    service_package_name: str = Field(..., description="Tên gói dịch vụ khi đăng ký IBMB")


class InternetBankingReceivePasswordInfo(BaseSchema):
    receive_password_code: str = Field(..., description="Mã hình thức nhân mật khẩu IBMB")
    receive_password_name: str = Field(..., description="Tên hình thức nhân mật khẩu IBMB")


class InternetBankingAuthenticationInfoItem(BaseSchema):
    authentication_code: str = Field(..., description="Mã loại xác thực khi giao dịch trên IB/MB")
    authentication_name: str = Field(..., description="Tên loại xác thực khi giao dịch trên IB/MB")


class InternetBankingAuthenticationInfoList(BaseSchema):
    ebank_ibmb_authentication_info_item: InternetBankingAuthenticationInfoItem


class InternetBankingBranchInfo(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ IBMB")


class GWRetrieveInternetBankingByCIFNumberResponse(BaseSchema):
    ebank_ibmb_username: str = Field(..., description="Tên đăng nhập dịch vụ IB/MB")
    ebank_ibmb_email: str = Field(..., description="Email khách hàng đăng ký sử dụng dịch vụ IBMB")
    ebank_ibmb_active_date: Union[datetime, str] = Field(..., description="Ngày kích hoạt dịch vụ IB/MB")
    ebank_ibmb_reg_date: Union[datetime, str] = Field(..., description="Ngày đăng ký dịch vụ IB/MB")
    ebank_ibmb_status: str = Field(..., description="Trạng thái dịch vụ IB/MB")
    ebank_ibmb_mobilephone: str = Field(..., description="Số điện thoại đăng ký dịch vụ IB/MB")
    ebank_ibmb_notify_mode: str = Field(..., description="Hình thức gửi tin nhắn (qua OTT hoặc SMS thông thường)")
    ebank_ibmb_latest_login: Union[datetime, str] = Field(..., description="Lần đăng nhập gần nhất trên dịch vụ IB/MB")
    ebank_ibmb_staff_info: InternetBankingStaffInfo = Field(..., description="Thông tin Nhân viên")
    ebank_ibmb_service_pack_info: InternetBankingServicePackInfo = Field(..., description="Thông tin Mã gói dịch vụ")
    ebank_ibmb_receive_password_info: InternetBankingReceivePasswordInfo = Field(..., description="Thông tin Cấp lại mật khẩu")
    ebank_ibmb_authentication_info_list: List[InternetBankingAuthenticationInfoList] = Field(..., description="Thông tin Xác thực khi giao dịch")
    ebank_ibmb_branch_info: InternetBankingBranchInfo = Field(..., description="Thông tin Đơn vị đăng ký dịch vụ")


class GWRetrieveInternetBankingByCIFNumberRequest(BaseSchema):
    cif_info: CifInfoRequest = Field(..., description="Dữ liệu đầu vào")


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
