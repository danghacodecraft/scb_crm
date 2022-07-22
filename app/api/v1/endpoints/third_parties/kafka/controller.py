import json

from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.kafka.repository import (
    repos_kafka_send_data
)


class CtrKafka(BaseController):
    def ctr_kafka_send_data(self, data_json: json):
        is_success, data = repos_kafka_send_data(data_json=data_json)
        if not is_success:
            return self.response_exception(msg=str(data))
        return data
