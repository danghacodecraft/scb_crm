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


class GetInitialPasswordMethod(str, Enum):
    SMS: str = 'SMS'
    Email: str = 'Email'


class AccountInformationResponse(BaseSchema):
    username: str = Field(..., description="Tên tài khoản Ebanking")
    receive_password_code: GetInitialPasswordMethod = Field(..., description='Hình thức nhận kích hoạt mật khẩu lần đầu')
    authentication_code_list: List[GetInitialAuthenticationCode] = Field(..., description='Hình thức xác thực')


class SMSCasaItemResposnse(BaseSchema):
    full_name: str = Field(..., description="Họ tên người nhận thông báo")
    mobile_number: str = Field(..., description="SĐT nhận thông báo")
    relationship_type_id: int = Field(..., description="Mối quan hệ")


class SMSCasaInfoResponse(BaseSchema):
    casa_id: str = Field(..., description="`id` của TKTT")
    sms_casa_items: List[SMSCasaItemResposnse] = Field(..., description="")


class EBankingResponse(BaseSchema):
    e_banking: AccountInformationResponse = Field(default=None, description='Thông tin E-Banking')
    sms_casa: List[SMSCasaInfoResponse] = Field(default=None, description="Thông tin đăng ký sms cho TKTT")


########################################################################################################################
# Request
########################################################################################################################
class MobileNumber(BaseSchema):
    mobile_number: str = Field(..., description='Số điện thoại', regex=REGULAR_PHONE_NUMBER)


class EBankingRequest(BaseSchema):
    username: str = Field(...)
    receive_password_code: GetInitialPasswordMethod = Field(..., description='Hình thức nhận kích hoạt mật khẩu lần đầu')
    authentication_code_list: List[GetInitialAuthenticationCode] = Field(..., description='Hình thức xác thực')


class EBankingSMSCasaRequest(BaseSchema):
    casa_account_id: str = Field(..., description='Số tài khoản Casa ảo')
    indentify_phone_num_list: List[MobileNumber] = Field(..., description='Danh sách số điện thoại đăng ký sử dụng dịch vụ SMS Banking')


class EBankingAndSMSCasaRequest(BaseSchema):
    ebank_info: Optional[EBankingRequest] = Field(..., description="")
    ebank_sms_casa_info: Optional[EBankingSMSCasaRequest] = Field(..., description="")
