from enum import Enum
from typing import List

from pydantic import Field, HttpUrl

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.tablet.web.schema import TabletMQTTResponse
from app.utils.constant.tablet import (
    LIST_BANNER_LANGUAGE_CODE_ENGLISH, LIST_BANNER_LANGUAGE_CODE_VIETNAMESE
)


class SyncWithWebByOTPDeviceInfoRequest(BaseSchema):
    mac_address: str = Field(..., description='Địa chỉ MAC của thiết bị')


class SyncWithWebByOTPRequest(BaseSchema):
    otp: str = Field(..., min_length=6, max_length=6, description='Mã OTP')
    device_info: SyncWithWebByOTPDeviceInfoRequest


class TellerInfoResponse(BaseSchema):
    avatar_url: str = Field(..., description='Đường dẫn avatar của giao dịch viên')
    full_name: str = Field(..., description='Tên của giao dịch viên')


class SyncWithWebByOTPResponse(BaseSchema):
    # otp_info: TabletOTPResponse
    mqtt_info: TabletMQTTResponse
    token: str = Field(..., description='Bearer token dùng để gọi các API sau khi đồng bộ thành công với web')
    branch_name: str = Field(..., description='Tên chi nhánh trên top bar')
    teller_info: TellerInfoResponse


class ListBannerLanguageCodeQueryParam(str, Enum):
    vi = LIST_BANNER_LANGUAGE_CODE_VIETNAMESE
    en = LIST_BANNER_LANGUAGE_CODE_ENGLISH


class ListBannerCategoryResponse(BaseSchema):
    category_name: str = Field(..., description='Tên loại')
    image_urls: List[HttpUrl] = Field(..., description='Danh sách link ảnh')
