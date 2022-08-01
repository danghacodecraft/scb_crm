from datetime import datetime
from typing import List, Union

from pydantic import Field

from app.api.base.schema import BaseSchema


# GW_retrieveIBInfoByCif
# request
class RetrieveIBInfoByCifInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Mã khách hàng", example='0008947')


class RetrieveIBInfoByCifRequest(BaseSchema):
    cif_info: RetrieveIBInfoByCifInfoRequest


# response
class RetrieveIBInfoByCifEbankStaffInfoResponse(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")


class RetrieveIBInfoByCifEbankServicePackInfoResponse(BaseSchema):
    service_package_code: str = Field(..., description="Mã gói dịch vụ khi đăng ký IBMB")
    service_package_name: str = Field(..., description="Tên gói dịch vụ khi đăng ký IBMB")


class RetrieveIBInfoByCifEbankReceivePasswordInfoResponse(BaseSchema):
    receive_password_code: str = Field(..., description="Mã hình thức nhân mật khẩu IBMB ")
    receive_password_name: str = Field(..., description="Tên hình thức nhận mật khẩu IBMB")


class RetrieveIBInfoByCifEbankAuthenticationInfoItemResponse(BaseSchema):
    authentication_code: str = Field(..., description="Mã loại xác thực khi giao dịch trên IB/MB")
    authentication_name: str = Field(..., description="Tên loại xác thực khi giao dịch trên IB/MB")


class RetrieveIBInfoByCifEbankAuthenticationInfoListResponse(BaseSchema):
    ebank_ibmb_authentication_info_item: RetrieveIBInfoByCifEbankAuthenticationInfoItemResponse


class RetrieveIBInfoByCifEbankBranchInfoResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ IBMB")


class RetrieveIBInfoByCifEbankInfoResponse(BaseSchema):
    ebank_ibmb_username: str = Field(..., description="Tên đăng nhập dịch vụ IB/MB")
    ebank_ibmb_email: str = Field(..., description="Email khách hàng đăng ký sử dụng dịch vụ IBMB")
    ebank_ibmb_active_date: Union[datetime, str] = Field(..., description="Ngày kích hoạt dịch vụ IB/MB")
    ebank_ibmb_reg_date: Union[datetime, str] = Field(..., description="Ngày đăng ký dịch vụ IB/MB")
    ebank_ibmb_status: str = Field(..., description="Trạng thái dịch vụ IB/MB")
    ebank_ibmb_mobilephone: str = Field(..., description="Số điện thoại đăng ký dịch vụ IB/MB")
    ebank_ibmb_notify_mode: str = Field(..., description="Hình thức gửi tin nhắn (qua OTT hoặc SMS thông thường)")
    ebank_ibmb_latest_login: Union[datetime, str] = Field(..., description="Lần đăng nhập gần nhất trên dịch vụ IB/MB")

    ebank_ibmb_staff_info: RetrieveIBInfoByCifEbankStaffInfoResponse
    ebank_ibmb_service_pack_info: RetrieveIBInfoByCifEbankServicePackInfoResponse
    ebank_ibmb_receive_password_info: RetrieveIBInfoByCifEbankReceivePasswordInfoResponse
    ebank_ibmb_authentication_info_list: List[RetrieveIBInfoByCifEbankAuthenticationInfoListResponse]
    ebank_ibmb_branch_info: RetrieveIBInfoByCifEbankBranchInfoResponse


class RetrieveIBInfoByCifResponse(BaseSchema):
    ebank_ibmb_info: List[RetrieveIBInfoByCifEbankInfoResponse]


########################################################################################################################

# GW checkUsernameIBMBExist


class CheckUsernameIBMBExistTransactionInfoItemRequest(BaseSchema):
    transaction_name: str = Field(..., description="Kênh eBank: `Internet Banking`, `Mobile Banking`, `SMS Banking`",
                                  example='Internet Banking')
    transaction_value: str = Field(..., description="Username đăng nhập IBMB", example='0945228866')


class CheckUsernameIBMBExistRequest(BaseSchema):
    transaction_info: CheckUsernameIBMBExistTransactionInfoItemRequest


class CheckUsernameIBMBExistEbankIBMBInfoItemResponse(BaseSchema):
    ebank_ibmb_status: str = Field(..., description="""Trạng thái khi kiểm tra username, nếu username có tồn tại:`UNAVAILABLE`, không tồn tại, có thể sử dụng dc: `AVAILABLE`
    """)


class CheckUsernameIBMBExistResponse(BaseSchema):
    ebank_ibmb_info: CheckUsernameIBMBExistEbankIBMBInfoItemResponse
