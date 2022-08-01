from datetime import date, datetime
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

# GW_retrieveMBInfoByCif
# request


class RetrieveMBInfoByCifInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Mã khách hàng", example='0008947')


class RetrieveMBInfoByCifRequest(BaseSchema):
    cif_info: RetrieveMBInfoByCifInfoRequest


# response


class RetrieveMBInfoByCifEbankStaffInfoResponse(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên")


class RetrieveMBInfoByCifEbankServicePackInfoResponse(BaseSchema):
    service_package_code: str = Field(..., description="Mã gói dịch vụ khi đăng ký IBMB")
    service_package_name: str = Field(..., description="Tên gói dịch vụ khi đăng ký IBMB")


class RetrieveMBInfoByCifEbankReceivePasswordInfoResponse(BaseSchema):
    receive_password_code: str = Field(..., description="Mã hình thức nhân mật khẩu IBMB ")
    receive_password_name: str = Field(..., description="Tên hình thức nhận mật khẩu IBMB")


class RetrieveMBInfoByCifEbankAuthenticationInfoItemResponse(BaseSchema):
    authentication_code: str = Field(..., description="Mã loại xác thực khi giao dịch trên IB/MB")
    authentication_name: str = Field(..., description="Tên loại xác thực khi giao dịch trên IB/MB")


class RetrieveMBInfoByCifEbankAuthenticationInfoListResponse(BaseSchema):
    ebank_ibmb_authentication_info_item: RetrieveMBInfoByCifEbankAuthenticationInfoItemResponse


class RetrieveMBInfoByCifEbankBranchInfoResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ IBMB")


class RetrieveMBInfoByCifEbankInfoResponse(BaseSchema):
    ebank_ibmb_username: str = Field(..., description="Tên đăng nhập dịch vụ IB/MB")
    ebank_ibmb_email: str = Field(..., description="Email khách hàng đăng ký sử dụng dịch vụ IBMB")
    ebank_ibmb_active_date: date = Field(..., description="Ngày kích hoạt dịch vụ IB/MB")
    ebank_ibmb_reg_date: date = Field(..., description="Ngày đăng ký dịch vụ IB/MB")
    ebank_ibmb_status: str = Field(..., description="Trạng thái dịch vụ IB/MB")
    ebank_ibmb_mobilephone: str = Field(..., description="Số điện thoại đăng ký dịch vụ IB/MB")
    ebank_ibmb_notify_mode: str = Field(..., description="Hình thức gửi tin nhắn (qua OTT hoặc SMS thông thường)")
    ebank_ibmb_latest_login: date = Field(..., description="Lần đăng nhập gần nhất trên dịch vụ IB/MB")

    ebank_ibmb_staff_info: RetrieveMBInfoByCifEbankStaffInfoResponse
    ebank_ibmb_service_pack_info: RetrieveMBInfoByCifEbankServicePackInfoResponse
    ebank_ibmb_receive_password_info: RetrieveMBInfoByCifEbankReceivePasswordInfoResponse
    ebank_ibmb_authentication_info_list: List[RetrieveMBInfoByCifEbankAuthenticationInfoListResponse]
    ebank_ibmb_branch_info: RetrieveMBInfoByCifEbankBranchInfoResponse


class RetrieveMBInfoByCifResponse(BaseSchema):
    ebank_ibmb_info: List[RetrieveMBInfoByCifEbankInfoResponse]


########################################################################################################################

# GW checkUsernameIBMBExist

# request
class CheckUsernameIBMBExistTransactionInfoItemRequest(BaseSchema):
    transaction_name: str = Field(..., description="Kênh eBank: `Internet Banking`, `Mobile Banking`, `SMS Banking`",
                                  example='Internet Banking')
    transaction_value: str = Field(..., description="Username đăng nhập IBMB", example='0945228866')


class CheckUsernameIBMBExistRequest(BaseSchema):
    transaction_info: CheckUsernameIBMBExistTransactionInfoItemRequest


# response

class CheckUsernameIBMBExistEbankIBMBInfoItemResponse(BaseSchema):
    ebank_ibmb_status: str = Field(..., description="""Trạng thái khi kiểm tra username, nếu username có tồn tại:`UNAVAILABLE`, không tồn tại, có thể sử dụng dc: `AVAILABLE`
    """)


class CheckUsernameIBMBExistResponse(BaseSchema):
    ebank_ibmb_info: CheckUsernameIBMBExistEbankIBMBInfoItemResponse


########################################################################################################################

# GW summaryBPTransByService

# request
class SummaryBPTransByServiceTransactionInfoRequest(BaseSchema):
    transaction_val_date: date = Field(..., description="Từ ngày", example='2022-04-15')
    transaction_val_date_to_date: date = Field(..., description="Đến ngày", example='2022-06-15')


class SummaryBPTransByServiceCIFInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF", example='135719')


class SummaryBPTransByServiceRequest(BaseSchema):
    transaction_info: SummaryBPTransByServiceTransactionInfoRequest
    cif_info: SummaryBPTransByServiceCIFInfoRequest


# response
class SummaryBPTransByServiceTopupServiceInfoResponse(BaseSchema):
    topup_service_name: str = Field(..., description="Tên dịch vụ topup. VD: Tiền điện, tiền nước, Internet,v.v...")
    topup_service_code: str = Field(..., description="Mã dịch vụ Topup")


class SummaryBPTransByServiceInvoiceTopupInfoItemResponse(BaseSchema):
    topup_service_info: SummaryBPTransByServiceTopupServiceInfoResponse
    topup_customer_code: str = Field(..., description="Mã khách hàng của dịch vụ topup")
    topup_count: str = Field(..., description="Số lượng giao dịch trong khoảng thời gian")


class SummaryBPTransByServiceInvoiceTopupInfoListResponse(BaseSchema):
    invoice_topup_info_item: SummaryBPTransByServiceInvoiceTopupInfoItemResponse


class SummaryBPTransByServiceResponse(BaseSchema):
    invoice_topup_info_list: List[SummaryBPTransByServiceInvoiceTopupInfoListResponse]


########################################################################################################################
# GW summaryBPTransByInvoice

# request

class SummaryBPTransByInvoiceTransactionInfoRequest(BaseSchema):
    transaction_val_date: date = Field(..., description="Từ ngày", example='2022-04-15')
    transaction_val_date_to_date: date = Field(..., description="Đến ngày", example='2022-06-15')


class SummaryBPTransByInvoiceCIFInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF", example='135719')


class SummaryBPTransByInvoiceRequest(BaseSchema):
    transaction_info: SummaryBPTransByInvoiceTransactionInfoRequest
    cif_info: SummaryBPTransByInvoiceCIFInfoRequest


# response

class SummaryBPTransByInvoiceInvoiceTopupInfoItemResponse(BaseSchema):
    topup_date_end: date = Field(..., description="Ngày giao dịch")
    topup_count: str = Field(..., description="Tổng số hóa đơn trong ngày")
    topup_amount: str = Field(..., description="Tổng số tiền giao dịch trong ngày")


class SummaryBPTransByInvoiceInvoiceTopupInfoListResponse(BaseSchema):
    invoice_topup_info_item: SummaryBPTransByInvoiceInvoiceTopupInfoItemResponse


class SummaryBPTransByInvoiceResponse(BaseSchema):
    invoice_topup_info_list: List[SummaryBPTransByInvoiceInvoiceTopupInfoListResponse]

########################################################################################################################
# GW selectBPTransByCif

# request


# response

########################################################################################################################
# GW openMB

# request
class OpenMBEbankIBMBInfoRequest(BaseSchema):
    ebank_ibmb_username: str = Field(..., description="Tên đăng nhập Mobile Banking",
                                     example='')
    ebank_ibmb_account_charge_fee: str = Field(..., description="Số tài khoản thanh toán",
                                               example='11223344')
    ebank_ibmb_mobilephone: str = Field(..., description="Số điện thoại nhận OTP,0933444938,0167,…",
                                        example='')
    ebank_ibmb_reg_date: date = Field(..., description="CreatedDate: Thời gian tạo user, "
                                                       " Format:yyyy-MM-dd "
                                                       "Ex: 2022-05-25",
                                      example='2022-05-25')


class OpenMBCIFInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF", example='')


class OpenMBAddressInfoRequest(BaseSchema):
    address_full: str = Field(..., description="Địa chỉ liên hệ", example='927 Trần Hưng Đạo, P.1, Q.5, TP.HCM')


class OpenMBCustomerInfoRequest(BaseSchema):
    full_name: str = Field(..., description="Họ tên khách hàng", example='HOÀNG THỊ DUNG')
    birthday: date = Field(..., description="Ngày sinh. Format yyyy-MM-dd ", example='1990-05-22')
    gender: str = Field(..., description="Giới tính: 1: Nam, 0: nữ", example='1')
    id_num: str = Field(..., description="Số CMTND/HC", example='033467895')
    email: str = Field(..., description="Email", example='hoangthidung@gmail.com')
    customer_vip_type: str = Field(..., description="Mã loại Khách hàng Ex: 000: Vip,….", example='001')


class OpenMBAccountInfoRequest(BaseSchema):
    account_type: str = Field(..., description="""Mã nhóm loại tài khoản
- U: tk thanh toán

- Y: tk tiết kiệm

- L: tk vay

- M: tk thẻ tín dụng""", example='U')
    account_type_name: date = Field(..., description="Mã Loại tài khoản", example='000')
    account_currency: str = Field(..., description="Loại tiền", example='VND')


class OpenMBAuthenticationSMSRequest(BaseSchema):
    authentication_code: str = Field(..., description="""Hình thức xác thực SMS
- 0: Không sử dụng,

- 1: Sử dụng""", example='1')


class OpenMBAuthenticationTokenRequest(BaseSchema):
    authentication_code: str = Field(..., description="""Hình thức xác thực Token
- 0: Không sử dụng,

- 1: Sử dụng""", example='00')
    authentication_name: str = Field(..., description="Giá trị của token", example='1950')


class OpenMBStaffRegRequest(BaseSchema):
    staff_code: str = Field(..., description="Mã nhân viên", example='00789')
    staff_name: str = Field(..., description="Họ tên nhân viên", example='LÊ THANH THẢN')


class OpenMBServicePackageInfoRequest(BaseSchema):
    service_package_code: str = Field(..., description="Mã gói dịch vụ MB", example='MC01')


class OpenMBStaffMakerInfoRequest(BaseSchema):
    staff_code: str = Field(..., description="User tạo tài khoản", example='HOANLKT')


class OpenMBStaffCheckerInfoRequest(BaseSchema):
    staff_code: str = Field(..., description="User duyệt tài khoản", example='KHANHLQ')


class OpenMBBranchCIFRequest(BaseSchema):
    branch_code: str = Field(..., description="Cif mở ở chi nhánh", example='001')


class OpenMBBranchRegRequest(BaseSchema):
    branch_code: str = Field(..., description="Chi nhánh của giao dịch viên tạo và duyệt tài khoản.", example='020')


class OpenMBRequest(BaseSchema):
    ebank_ibmb_info: OpenMBEbankIBMBInfoRequest
    comfirm_date: date = Field(..., description="CreatedDate: Thời gian tạo user, "
                                                " Format:yyyy-MM-dd "
                                                "Ex: 2022-05-25 ", example='2022-05-25')
    cif_info: OpenMBCIFInfoRequest
    address_info: OpenMBAddressInfoRequest
    customer_info: OpenMBCustomerInfoRequest
    account_info: OpenMBAccountInfoRequest
    authentication_sms: OpenMBAuthenticationSMSRequest
    authentication_token: OpenMBAuthenticationTokenRequest
    staff_reg: OpenMBStaffRegRequest
    service_package_info: OpenMBServicePackageInfoRequest
    staff_maker: OpenMBStaffMakerInfoRequest
    staff_checker: OpenMBStaffCheckerInfoRequest
    branch_cif: OpenMBBranchCIFRequest
    branch_reg: OpenMBBranchRegRequest

# response

########################################################################################################################
# GW selectServicePackIB

# request


# response

########################################################################################################################
