from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.kafka.repository import (
    repos_kafka_send_data
)


class CtrKafka(BaseController):
    async def ctr_kafka_send_data(self, data: dict):
        send_data_info = self.call_repos(await repos_kafka_send_data(data=data))
        return send_data_info
