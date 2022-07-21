from app.third_parties.services.kafka import ServiceKafka


def repos_kafka_send_data(data: dict):
    send_data_info = ServiceKafka().send_data(data=data)
    return send_data_info
