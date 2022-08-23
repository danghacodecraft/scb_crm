from datetime import datetime
from enum import Enum
from typing import Dict, List, Union

from pydantic import Field, HttpUrl

from app.api.base.schema import BaseSchema
from app.utils.constant.tablet import (
    MOBILE_ACTION_ENTER_IDENTITY_NUMBER, MOBILE_ACTION_NEW_TRANSACTION,
    MOBILE_ACTION_PROCESS_TRANSACTION, MOBILE_ACTION_SIGN,
    MOBILE_ACTION_TAKE_DOCUMENT_PHOTO, MOBILE_ACTION_TAKE_FACE_PHOTO,
    MOBILE_ACTION_TRANSACT_SUCCESS
)


class TabletOTPResponse(BaseSchema):
    otp: str = Field(..., min_length=6, max_length=6, description='Mã OTP')
    expired_after_in_seconds: int = Field(..., description="Hết hạn sau bao nhiêu giây")
    expired_at: datetime = Field(..., description="Hết hạn lúc")


class TabletMQTTResponse(BaseSchema):
    host: str = Field(..., description='domain')
    vhost: str = Field(..., description='vhost')
    port: int = Field(..., description='port')
    username: str = Field(..., description='username')
    password: str = Field(..., description='password')
    topic_name: str = Field(..., description='topic_name')


class TabletOTPAndMqttInfoResponse(BaseSchema):
    otp_info: TabletOTPResponse
    web_stomp_info: TabletMQTTResponse


########################################################################################################################
# model dùng khi validate extra_data API switch to other screen in tablet
########################################################################################################################
class TabletActionProcessDataExtraData(BaseSchema):
    transaction_name: str = Field(..., description='Tên giao dịch')


class TabletActionSignDocumentExtraData(BaseSchema):
    name: str = Field(..., description='Tên biểu mẫu')
    file_url: HttpUrl = Field(..., description='Đường dẫn tới file pdf của biểu mẫu sau khi đổ dữ liệu')


class TabletActionSignExtraData(BaseSchema):
    documents: List[TabletActionSignDocumentExtraData] = Field(..., description='Danh sách các biểu mẫu cần ký')
########################################################################################################################


class TabletAction(str, Enum):
    mobile_action_enter_identity_number = MOBILE_ACTION_ENTER_IDENTITY_NUMBER
    mobile_action_take_document_photo = MOBILE_ACTION_TAKE_DOCUMENT_PHOTO
    mobile_action_take_face_photo = MOBILE_ACTION_TAKE_FACE_PHOTO
    mobile_action_process_transaction = MOBILE_ACTION_PROCESS_TRANSACTION
    mobile_action_new_transaction = MOBILE_ACTION_NEW_TRANSACTION
    mobile_action_sign = MOBILE_ACTION_SIGN
    mobile_action_transact = MOBILE_ACTION_TRANSACT_SUCCESS


class TabletSwitchScreenRequest(BaseSchema):
    action: TabletAction = Field(..., description='Hành động tương ứng bên tablet')
    extra_data: Union[Dict, TabletActionProcessDataExtraData, TabletActionSignExtraData] = Field(..., description='Thông tin thêm cho hành động tương ứng bên tablet')


class TabletStatusResponse(BaseSchema):
    status: bool = Field(..., description='Kết quả')
