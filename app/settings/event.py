from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.settings.service import SERVICE
from app.third_parties.services.ekyc import ServiceEKYC
from app.third_parties.services.file import ServiceFile
from app.third_parties.services.gw import ServiceGW
from app.third_parties.services.idm import ServiceIDM
from app.third_parties.services.kafka import ServiceKafka
from app.third_parties.services.rabbitmq import ServiceRabbitmq
from app.third_parties.services.redis import ServiceRedis

INIT_SERVICE = SERVICE
service_file = ServiceFile(init_service=INIT_SERVICE)
service_ekyc = ServiceEKYC(init_service=INIT_SERVICE)
service_gw = ServiceGW(init_service=INIT_SERVICE)
service_idm = ServiceIDM(init_service=INIT_SERVICE)
service_kafka = ServiceKafka(init_service=INIT_SERVICE)
service_redis = ServiceRedis(init_service=INIT_SERVICE)
service_rabbitmq = ServiceRabbitmq(init_service=INIT_SERVICE)



def create_start_app_handler(app: FastAPI) -> Callable:  # noqa
    async def start_app():
        service_file.start()
        service_ekyc.start()
        service_gw.start()
        service_idm.start()
        service_redis.start()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # noqa
    @logger.catch
    async def stop_app() -> None:
        await service_file.stop()
        await service_ekyc.stop()
        await service_gw.stop()
        await service_redis.stop()
        service_rabbitmq.stop()

    return stop_app
