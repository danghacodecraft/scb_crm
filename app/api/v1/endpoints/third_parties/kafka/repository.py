import json

from app.third_parties.services.kafka import ServiceKafka


def repos_kafka_send_data(data_json: json):
    send_data_info = ServiceKafka().send_data(data_json=data_json)
    return send_data_info
