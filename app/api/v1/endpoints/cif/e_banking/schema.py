from enum import Enum
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
########################################################################################################################
# Response
########################################################################################################################
from app.utils.constant.validate import REGULAR_PHONE_NUMBER


class GetInitialAuthenticationCode(str, Enum):
    XACTHUC_SMS: str = 'SMS'
    XACTHUC_SOFTTOKEN: str = 'SOFT_TOKEN'
    XACTHUC_HARDTOKEN: str = 'HARD_TOKEN'


class GetInitialSMSNotifyCode(str, Enum):
    ALL: str = 'ALL'
    BDSD: str = 'BDSD'
    RT: str = 'RT'
    NT: str = 'NT'
    TTTK: str = 'TTTK'


class GetInitialSMSRegistryBalanceOptionResponse(str, Enum):
    OTT: str = 'OTT'
    SMS: str = 'SMS'


class GetInitialPasswordMethod(str, Enum):
    SMS: str = 'SMS'
    Email: str = 'Email'


class AccountInformationResponse(BaseSchema):
    username: str = Field(..., description="Tên tài khoản Ebanking")
    receive_password_code: GetInitialPasswordMethod = Field(..., description='Hình thức nhận kích hoạt mật khẩu lần đầu')
    authentication_code_list: List[GetInitialAuthenticationCode] = Field(..., description='Hình thức xác thực')


class SMSCasaCustomerInfoResponse(BaseSchema):
    main_phone_number: str = Field(..., description='Số điện thoại', regex=REGULAR_PHONE_NUMBER)
    customer_full_name: str = Field(..., description="Họ tên")


class SMSCasaRelationshipItemResponse(BaseSchema):
    mobile_number: str = Field(..., description="SĐT nhận thông báo", regex=REGULAR_PHONE_NUMBER)
    relationship_type_id: str = Field(..., description="Mối quan hệ")
    full_name: str = Field(..., description="Họ tên người nhận thông báo")


class SMSCasaItemResponse(BaseSchema):
    casa_id: str = Field(..., description="`id` của TKTT")
    main_phone_number_info: Optional[SMSCasaCustomerInfoResponse] = Field(..., description="Thông tin SĐT, chủ tài khoản đăng ký sms")
    receiver_noti_relationship_items: List[SMSCasaRelationshipItemResponse] = Field(description="Thông tin SĐT và MQH đăng ký sms")
    notify_code_list: List[GetInitialSMSNotifyCode] = Field(description="Tùy chọn thông báo")


class SMSCasaInfoResponse(BaseSchema):
    reg_balance_options: List[GetInitialSMSRegistryBalanceOptionResponse] = Field(..., description='Thông báo OTT - SMS')
    registry_balance_items: List[SMSCasaItemResponse] = Field(..., description="")


class EBankingResponse(BaseSchema):
    e_banking: Optional[AccountInformationResponse] = Field(..., description='Thông tin E-Banking')
    sms_casa: Optional[SMSCasaInfoResponse] = Field(..., description="Thông tin đăng ký sms cho TKTT")


########################################################################################################################
# Request
########################################################################################################################
class EBankingRequest(BaseSchema):
    username: str = Field(...)
    receive_password_code: GetInitialPasswordMethod = Field(..., description='Hình thức nhận kích hoạt mật khẩu lần đầu')
    authentication_code_list: List[GetInitialAuthenticationCode] = Field(..., description='Hình thức xác thực')


class SMSCasaCustomerInfoRequest(BaseSchema):
    main_phone_number: str = Field(..., description='Số điện thoại', regex=REGULAR_PHONE_NUMBER)
    customer_full_name: str = Field(..., description="Họ tên")


class SMSCasaRelationshipItemRequest(BaseSchema):
    mobile_number: str = Field(..., description="SĐT nhận thông báo", regex=REGULAR_PHONE_NUMBER)
    full_name: str = Field(..., description="Họ tên người nhận thông báo")
    relationship_type_id: str = Field(..., description="Mối quan hệ")


class SMSCasaItemRequest(BaseSchema):
    casa_id: str = Field(..., description="`id` của TKTT")
    main_phone_number_info: SMSCasaCustomerInfoRequest = Field(..., description="Thông tin SĐT, chủ tài khoản đăng ký sms")
    receiver_noti_relationship_items: List[SMSCasaRelationshipItemRequest] = Field(..., description="Thông tin SĐT và MQH đăng ký sms")
    notify_code_list: List[GetInitialSMSNotifyCode] = Field(..., description="Tùy chọn thông báo")


class EBankingSMSCasaRequest(BaseSchema):
    reg_balance_options: List[GetInitialSMSRegistryBalanceOptionResponse] = Field(..., description='Thông báo OTT - SMS')
    registry_balance_items: List[SMSCasaItemRequest] = Field(..., description="")
