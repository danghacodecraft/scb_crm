import json

import pika

from app.utils.constant.tablet import RABBITMQ_EXCHANGE_AMQ_TOPIC


class ServiceRabbitmq:
    def __init__(self, init_service):
        rabbitmq_config = init_service['rabbitmq']
        self.host = rabbitmq_config['host_ip']
        self.vhost = rabbitmq_config['vhost']
        self.port = int(rabbitmq_config['amqp_port'])
        self.username = rabbitmq_config['server_username']
        self.password = rabbitmq_config['server_password']

        self.connection = None
        self.channel = None

    def create_connection(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=pika.credentials.PlainCredentials(self.username, self.password)
            )
        )
        self.channel = self.connection.channel()

    def stop(self):
        if self.connection:
            self.connection.close()

    def publish(self, message, routing_key):
        if not self.connection or self.connection.is_closed:
            self.create_connection()

        if isinstance(message, dict):
            message = json.dumps(message)

        self.channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE_AMQ_TOPIC,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(content_type='application/json')
        )
