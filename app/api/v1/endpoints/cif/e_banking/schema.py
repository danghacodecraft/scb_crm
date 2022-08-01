from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse
########################################################################################################################
# Response
########################################################################################################################
from app.utils.constant.validate import REGULAR_PHONE_NUMBER


class ContactTypeResponse(BaseSchema):
    id: str = Field(..., description='Mã loại dữ liệu liên hệ')
    name: str = Field(..., description='Tên loại liên hệ')
    group: str = Field(..., description='Nhóm loại liên hệ')
    description: str = Field(..., description='Mô tả loại  liệu liên hệ')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NotificationCasaRelationshipResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh')
    mobile_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt')
    relationship_type: DropdownResponse = Field(..., description='Mối quan hệ')


class EBankingNotificationResponse(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class RegisterBalanceCasa(BaseSchema):
    account_id: Optional[str] = Field(..., description='Số tài khoản')
    # EBankingRegisterBalance.name (Tên Đăng ký Biến động số dư các loại tài khoản)
    checking_account_name: str = Field(..., description='Tên tài khoản')
    primary_phone_number: str = Field(..., description='Số điện thoại')
    full_name_vn: str = Field(..., description='Tên tiếng việt ')
    primary_mobile_number: DropdownResponse = Field(None, description='Loại SĐT')
    notification_casa_relationships: List[NotificationCasaRelationshipResponse] = Field(..., description='Mối quan hê')
    e_banking_notifications: List[EBankingNotificationResponse] = Field(..., description='Hình thức nhận thông báo')


class BalancePaymentAccountResponse(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: List[ContactTypeResponse] = Field(..., description='Hình thức nhận thông báo')
    register_balance_casas: List[RegisterBalanceCasa] = Field(..., description='Thông tin tài khoản nhận thông báo')


class TdAccount(BaseSchema):
    id: str = Field(..., description='Mã định danh')
    number: str = Field(..., description='Số tài khoản')
    name: str = Field(..., description='Tên khách hàng')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class TdAccountResponse(BaseSchema):
    td_accounts: List[TdAccount] = Field(..., description='Danh sách số tài khoản tiết kiệm')
    page: int = Field(..., description='Trang')
    limit: int = Field(..., description='Giới hạn')
    total_page: int = Field(..., description='Tổng số trang')


class BalanceSavingAccountResponse(BaseSchema):
    register_flag: Optional[bool] = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    customer_contact_types: Optional[List[ContactTypeResponse]] = Field(..., description='Hình thức nhận thông báo')
    mobile_number: Optional[str] = Field(..., description='Số điện thoại')
    range: Optional[TdAccountResponse] = Field(..., description='Phạm vi áp dụng')
    e_banking_notifications: Optional[List[EBankingNotificationResponse]] = Field(...,
                                                                                  description='Hình thức nhận thông báo')


class GetInitialPasswordMethod(str, Enum):
    SMS: str = 'SMS'
    Email: str = 'Email'


class MethodAuthentication(DropdownResponse):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NumberResponse(BaseSchema):
    id: Optional[str] = Field(..., description='Mã tài khoản', nullable=True)
    name: Optional[str] = Field(..., description='Tài khoản', nullable=True)


class OptionalEBankingAccountResponse(BaseSchema):
    reset_password_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    active_account_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    note: str = Field(..., description='Mô tả')
    updated_by: str = Field(..., description='Người cập nhật')
    updated_at: datetime = Field(..., description='Cập nhật vào lúc, format dạng: `YYYY-mm-dd HH:MM:SS`',
                                 example='2021-15-12 06:07:08')


class PaymentFee(BaseSchema):
    flag: bool = Field(..., description='Trạng thái. `False`: Tiền mặt. `True`: Trích từ tài khoản')
    account: str = Field(None, description='Số tài khoản trích từ tài khoản', allow_null=True)


class AccountInformation(BaseSchema):
    register_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    account_name: str = Field(..., description='Tên đăng nhập')
    get_initial_password_method: GetInitialPasswordMethod = Field(...,
                                                                  description='Hình thức nhận  mật khẩu kích hoạt')
    method_authentication: List[MethodAuthentication] = Field(..., description='Hình thức xác thực')
    charged_account: Optional[str] = Field(None, description='Tài khoản thanh toán phí', nullable=True)
    payment_fee: Optional[PaymentFee] = Field(None, description='Thanh toán phí', nullable=True)


class AccountInformationResponse(BaseSchema):
    account_information: AccountInformation = Field(..., description='Tài khoản E-Banking')
    optional_e_banking_account: Optional[OptionalEBankingAccountResponse] = Field(
        None,
        description='Hình thức nhận thông báo',
        nullable=True
    )


class EBankingResponse(BaseSchema):
    change_of_balance_payment_account: BalancePaymentAccountResponse = Field(..., description='Tài khoản thanh toán')
    change_of_balance_saving_account: Optional[BalanceSavingAccountResponse] = Field(None,
                                                                                     description='Tài khoản tiết kiệm')
    e_banking_information: AccountInformationResponse = Field(..., description='Thông tin E-Banking')


################################################################
# Danh sách tài khoản thanh toán
################################################################
class BalancePaymentAccountResponses(BaseSchema):
    id: str = Field(..., description='Mã định danh tài khoản thanh toán')
    account_number: Optional[str] = Field(..., description='Số tài khoản thanh toán')
    product_name: str = Field(..., description='Tên sản phẩm tài khoản thanh toán')
    # checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


# Chi tiết cấp lại mật khẩu E-Banking call center -> I. Thông tin cá nhân khách hàng -> 1. Hình thức nhận mật khẩu mới
class EBankingResetPasswordMethod(DropdownResponse):
    checked_flag: bool = Field(..., description="Cờ xác nhận hình thức nhận mật khẩu")


# Chi tiết cấp lại mật khẩu E-Banking call center -> I. Thông tin cá nhân khách hàng
class PersonalCustomerInformationResponse(BaseSchema):
    id: str = Field(..., description="ID")
    cif_number: str = CustomField().CIFNumberField
    customer_classification: DropdownResponse = Field(..., description="Loại khách hàng (VD: Cá Nhân)")
    avatar_url: Optional[str] = Field(..., description="URL Avatar khách hàng")
    full_name: str = Field(..., description="Tên khách hàng không dấu")
    gender: DropdownResponse = Field(..., description="Giới tính")
    email: Optional[str] = Field(..., description="Email")
    mobile_number: str = Field(..., description="Số điện thoại")
    identity_number: str = Field(..., description="CMND/CCCD")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    issued_date: date = Field(..., description="Ngày cấp")
    expired_date: date = Field(..., description="Ngày hết hạn")
    address: str = Field(..., description="Địa chỉ")
    e_banking_reset_password_method: List[EBankingResetPasswordMethod] = Field(
        ..., description="1. Hình thức nhận mật khẩu mới"
    )
    e_banking_account_name: str = Field(..., description="2. Tên đăng nhập")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> I. Câu hỏi cơ bản 1
# -> 1. Loại thẻ(tên thẻ, màu thẻ)
class BranchOfCardResponse(DropdownResponse):
    color: DropdownResponse = Field(..., description="Màu thẻ")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> I. Câu hỏi cơ bản 1
class BasicQuestion1Response(BaseSchema):
    branch_of_card: BranchOfCardResponse = Field(..., description="1. Loại thẻ(tên thẻ, màu thẻ)")
    sub_card_number: str = Field(..., description="2. Số lượng thẻ phụ")
    mobile_number: str = Field(..., description="3. SĐT đăng ký dịch vụ")
    branch: DropdownResponse = Field(..., description="4. Đơn vị đăng ký dịch vụ/ mở TK")
    method_authentication: DropdownResponse = Field(..., description="5. Hình thức xác thực mật khẩu")
    e_banking_account_name: str = Field(..., description="6. Tên đăng nhập IB/MB")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2 -> 2. Hạn mức thẻ
class CreditLimitResponse(BaseSchema):
    value: str = Field(..., description="Hạn mức đã sử dụng của Thẻ tín dụng")
    currency: DropdownResponse = Field(..., description="Loại tiền")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2
# -> 4. Câu hỏi bí mật/Người liên hệ
class SecretQuestionOrPersonalRelationshipResponse(BaseSchema):
    customer_relationship: DropdownResponse = Field(..., description="URL tài liệu đi kèm")
    mobile_number: str = Field(..., description="URL tài liệu đi kèm")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> II. Câu hỏi cơ bản 2
class BasicQuestion2Response(BaseSchema):
    last_four_digits: str = Field(..., description="1. 4 số cuối của thẻ")
    credit_limit: CreditLimitResponse = Field(..., description="2. Hạn mức thẻ")
    email: Optional[str] = Field(..., description="3. Email đăng ký")
    secret_question_or_personal_relationships: List[SecretQuestionOrPersonalRelationshipResponse] = Field(
        ..., description="4. Câu hỏi bí mật/ Người liên hệ")
    automatic_debit_status: str = Field(..., description="5. Tình trạng đăng ký trích nợ tự động")
    transaction_method_receiver: DropdownResponse = Field(..., description="6. Hình thức nhận sao kê")


class Nearest3rdSecureResponse(CreditLimitResponse):
    business_partner: DropdownResponse = Field(..., description="Đối tác kinh doanh")


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi -> III. Câu hỏi nâng cao
class AdvancedQuestionResponse(BaseSchema):
    used_limit_of_credit_card: CreditLimitResponse = Field(..., description="1. Hạn mức đã sử dụng của Thẻ tín dụng")
    nearest_3d_secure: Nearest3rdSecureResponse = Field(
        ..., description="2. Thông tin GD Thẻ tín dụng có 3D Secure gần nhất"
    )
    one_of_two_nearest_successful_transaction: str = Field(
        ..., description="""3. Thông tin 1 trong 2 GD phát sinh trong thành công gần nhất
        ( đối với thẻ ghi nợ, thẻ tín dụng, TKTT, dịch vụ IB/MB) """
    )
    nearest_successful_login_time: str = Field(
        ..., description="4. Thời gian đăng nhập dịch vụ IB/MB thành công gần nhất"
    )


# Chi tiết cấp lại mật khẩu E-Banking call center -> II. Danh sách câu hỏi
class QuestionResponse(BaseSchema):
    basic_question_1: BasicQuestion1Response = Field(..., description="I. Câu hỏi cơ bản 1")
    basic_question_2: BasicQuestion2Response = Field(..., description="II. Câu hỏi cơ bản 2")
    advanced_question: AdvancedQuestionResponse = Field(..., description="III. Câu hỏi nâng cao")


# Chi tiết cấp lại mật khẩu E-Banking call center -> IV. Kết luận
class ResultResponse(BaseSchema):
    confirm_current_transaction_flag: bool = Field(..., description="Cờ xác nhận thực hiện giao dịch")
    note: str = Field(..., description="Ghi chú")


# Chi tiết cấp lại mật khẩu E-Banking call center
class ResetPasswordEBankingResponse(BaseSchema):
    personal_customer_information: PersonalCustomerInformationResponse = Field(
        ..., description="I. Thông tin cá nhân khách hàng"
    )
    question: QuestionResponse = Field(..., description="II. Danh sách câu hỏi")
    document_url: str = Field(..., description="III. Phiếu yêu cầu của đơn vị - URL tài liệu đi kèm")
    result: ResultResponse = Field(..., description="IV. Kết luận")


########################################################################################################################
# Request
########################################################################################################################

class ContactTypeRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NotificationCasaRelationshipRequest(BaseSchema):
    mobile_number: str = Field(..., description='Số điện thoại', regex=REGULAR_PHONE_NUMBER)
    full_name_vn: str = Field(..., description='Tên tiếng việt', max_length=100)
    relationship_type: DropdownRequest = Field(..., description='Mối quan hệ')


class EBankingNotificationRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class AccountRequest(BaseSchema):
    id: str = Field(..., description='Mã định danh tài khoản')
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class TdAccountRequest(BaseSchema):
    td_accounts: List[AccountRequest] = Field(..., description='Danh sách số tài khoản tiết kiệm')


class ResetPasswordMethodRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class MethodAuthenticationRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')


class NumberRequest(BaseSchema):
    id: Optional[str] = Field(..., description='Mã tài khoản', nullable=True)


class PaymentFeeRequest(DropdownRequest):
    checked_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    number: NumberRequest = Field(..., description='Tài khoản thanh toán')


class OptionalEBankingAccountRequest(BaseSchema):
    reset_password_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    active_account_flag: bool = Field(..., description='Trạng thái. `False`: Không. `True`: Có')
    note: str = Field(..., description='Mô tả')


class AccountInformationEBankingRequest(BaseSchema):
    account_information: AccountInformation = Field(..., description='Tài khoản E-Banking')


class GetInitialAuthenticationCode(str, Enum):
    XACTHUC_SMS: str = 'SMS'
    XACTHUC_SOFTTOKEN: str = 'SOFT_TOKEN'
    XACTHUC_HARDTOKEN: str = 'HARD_TOKEN'


class MobileNumber(BaseSchema):
    mobile_number: str = Field(..., description='Số điện thoại', regex=REGULAR_PHONE_NUMBER)


class EBankingRequest(BaseSchema):
    username: str = Field(...)
    receive_password_code: GetInitialPasswordMethod = Field(...)
    authentication_code_list: List[GetInitialAuthenticationCode] = Field(..., description='Hình thức xác thực')


class EBankingSMSCasaRequest(BaseSchema):
    casa_account_id: str = Field(..., description='Số tài khoản Casa ảo')
    indentify_phone_num_list: List[MobileNumber] = Field(..., description='Danh sách số điện thoại đăng ký sử dụng dịch vụ SMS Banking')


class EBankingAndSMSCasaRequest(BaseSchema):
    ebank_info: Optional[EBankingRequest] = Field(..., description="")
    ebank_sms_casa_info: Optional[EBankingSMSCasaRequest] = Field(..., description="")


class BalanceSavingAccountsResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh tài khoản')
    account_number: str = Field(..., description='Số tài khoản')
    name: str = Field(..., description='Tên người sở hữu tài khoản')
    # checked_flag: bool = Field(..., description='Trạng thái đăng ký. `False`: Không. `True`: Có')


class DocumentResponse(BaseSchema):
    id: str = Field(..., description='Mã định danh biểu mẫu')
    name: str = Field(..., description='Tên biểu mẫu')
    url: str = Field(..., description='Đường dẫn biểu mẫu')
    version: str = Field(..., description='Phiên bản biểu mẫu')
    created_by: str = Field(..., description='Người tạo')
    created_at: datetime = Field(..., description='Thời gian tạo')
    active_flag: bool = Field(..., description='Trạng thái đăng ký. `False`: Không. `True`: Có')


class ResetPasswordTellerResponse(BaseSchema):
    personal_customer_information: PersonalCustomerInformationResponse = Field(
        ..., description='Thông tin cá nhân khách hàng'
    )
    document: DocumentResponse = Field(..., description='Thông tin biểu mẫu')
