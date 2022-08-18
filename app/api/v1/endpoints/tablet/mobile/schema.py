from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.tablet.web.schema import TabletMQTTResponse


class SyncWithWebByOTPDeviceInfoRequest(BaseSchema):
    mac_address: str = Field(..., description='Địa chỉ MAC của thiết bị')


class SyncWithWebByOTPRequest(BaseSchema):
    otp: str = Field(..., min_length=6, max_length=6, description='Mã OTP')
    device_info: SyncWithWebByOTPDeviceInfoRequest


class SyncWithWebByOTPResponse(BaseSchema):
    # otp_info: TabletOTPResponse
    mqtt_info: TabletMQTTResponse
    token: str = Field(..., description='Bearer token dùng để gọi các API sau khi đồng bộ thành công với web')
