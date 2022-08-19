import math
import random

from app.settings.event import INIT_SERVICE
from app.utils.constant.tablet import DEVICE_TYPE_MOBILE, DEVICE_TYPE_WEB


def generate_otp(length: int = 6):
    digits = "0123456789"
    otp = ""

    # length of password can be changed
    # by changing value in range
    for _ in range(length):
        otp += digits[math.floor(random.random() * 10)]

    return otp


def get_client_broker_config_info(device_type: str):
    return {
        'host': INIT_SERVICE['rabbitmq']['host_name'],
        'vhost': INIT_SERVICE['rabbitmq']['vhost'],
        'port': INIT_SERVICE['rabbitmq']['mqtt_port' if device_type == DEVICE_TYPE_MOBILE else 'web_stomp_port'],
        'username': INIT_SERVICE['rabbitmq']['client_username'],
        'password': INIT_SERVICE['rabbitmq']['client_password'],
        'topic_name': '',
    }


def get_topic_name(device_type: str, tablet_id: str, otp: str):
    if device_type not in [DEVICE_TYPE_WEB, DEVICE_TYPE_MOBILE]:
        return None

    return f"{device_type}.{tablet_id}{otp}"
