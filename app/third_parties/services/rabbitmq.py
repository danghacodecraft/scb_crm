import pika

from app.utils.constant.tablet import RABBITMQ_EXCHANGE_AMQ_TOPIC
from app.utils.functions import orjson_dumps


class ServiceRabbitmq:
    def __init__(self, init_service):
        rabbitmq_config = init_service['rabbitmq']
        self.host = rabbitmq_config['host_ip']
        self.vhost = rabbitmq_config['vhost']
        self.port = int(rabbitmq_config['amqp_port'])
        self.username = rabbitmq_config['server_username']
        self.password = rabbitmq_config['server_password']

    def publish(self, message, routing_key):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=pika.credentials.PlainCredentials(self.username, self.password)
            )
        )
        channel = connection.channel()

        if isinstance(message, dict):
            message = orjson_dumps(message)

        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE_AMQ_TOPIC,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(content_type='application/json')
        )

        connection.close()
