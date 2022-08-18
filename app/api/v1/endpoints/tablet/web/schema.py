from datetime import datetime

from pydantic import Field

from app.api.base.schema import BaseSchema


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
    mqtt_info: TabletMQTTResponse
