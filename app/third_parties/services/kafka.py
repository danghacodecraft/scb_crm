import json
from datetime import date, datetime

import orjson
from confluent_kafka import Producer
from dotenv import dotenv_values
from loguru import logger
from starlette import status

from app.api.base.except_custom import ExceptionHandle
from app.settings.config import WRITE_LOG
from app.utils.functions import date_to_string, datetime_to_string, now

config = dotenv_values('.env')


def orjson_default(o):
    # See "Date Time String Format" in the ECMA-262 specification.
    if isinstance(o, datetime):
        return datetime_to_string(o, _format='%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(o, date):
        return date_to_string(o)
    # elif isinstance(o, ErrorDetail):
    #     return str(o)
    else:
        raise TypeError


class ServiceKafka:
    def __init__(self, kafka_message=None):
        self.kafka_message = kafka_message
        if self.kafka_message is None:
            self.kafka_message = {}

        self.producer = Producer({
            # không handle lỗi để config sai .env thì raise luôn
            "bootstrap.servers": ",".join(json.loads(config.get("KAFKA_BOOTSTRAP_SERVERS"))),
            "security.protocol": config.get("KAFKA_SECURITY_PROTOCOL"),
            "sasl.mechanism": config.get("KAFKA_SASL_MECHANISM"),
            "sasl.username": config.get("KAFKA_SASL_PLAIN_USERNAME"),
            "sasl.password": config.get("KAFKA_SASL_PLAIN_PASSWORD"),
            "message.max.bytes": config.get("KAFKA_MESSAGE_MAX_BYTES")
        })
        self.default_topic = config.get("KAFKA_PRODUCER_TOPIC")

        if WRITE_LOG and kafka_message:
            logger.debug("Started send message to KAFKA")
            self.send_message(data={
                'kafka_created_at': datetime_to_string(now()),
                'message': self.kafka_message
            })

    @staticmethod
    def ack(err, msg):
        if err is not None:
            logger.error(f"Failed to deliver message: {msg}: {err}")
        else:
            logger.info("Message produced success")

    def send_message(self, data: dict, topic=None):
        try:
            self.producer.produce(
                topic=topic if topic else self.default_topic,
                value=orjson.dumps(data, default=orjson_default, option=orjson.OPT_PASSTHROUGH_DATETIME),
                callback=self.ack
            )

            # Wait up to 1 second for events. Callbacks will be invoked during
            # this method call if the message is acknowledged.
            self.producer.poll(1)
        except Exception as e:
            raise ExceptionHandle(
                errors=[{'loc': None, 'msg': 'confluent_kafka.Error', 'detail': str(e)}],
                status_code=status.HTTP_400_BAD_REQUEST
            )
