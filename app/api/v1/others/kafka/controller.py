from kafka import KafkaProducer

from app.utils.functions import orjson_dumps


class Kafka:
    def __init__(self):
        self.sasl_mechanism = 'PLAIN'
        self.security_protocol = 'SASL_PLAINTEXT'
        self.bootstrap_servers = ['192.168.73.139:9092']    # server name
        self.sasl_plain_username = "admin"
        self.sasl_plain_password = "admin"

    def send_data(self, data: dict, topic: str = 'CRM_BE'):
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=orjson_dumps(data),
            sasl_mechanism=self.sasl_mechanism,
            security_protocol=self.security_protocol,
            sasl_plain_username=self.sasl_plain_username,
            sasl_plain_password=self.sasl_plain_password
        )
        producer.send(topic=topic, value=data)
