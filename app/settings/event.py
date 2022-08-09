from typing import Callable

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import select

from app.third_parties.oracle.base import SessionLocal
from app.third_parties.oracle.models.env.model import DBS
from app.third_parties.services.ekyc import ServiceEKYC
from app.third_parties.services.file import ServiceFile
from app.third_parties.services.gw import ServiceGW
from app.third_parties.services.idm import ServiceIDM
from app.third_parties.services.kafka import ServiceKafka
from app.third_parties.services.redis import ServiceRedis

ss = SessionLocal()
configs = ss.execute(
    select(
        DBS
    )
    .order_by(DBS.server_name)
).scalars().all()
SERVICE = {}
for config in configs:
    config_data = {config.name: config.value}
    if not config.server_name:
        SERVICE.update(config_data)
    elif config.server_name not in SERVICE:
        SERVICE.update({config.server_name: {config.name: config.value}})
    else:
        SERVICE[config.server_name][config.name] = config.value

service_file = ServiceFile(init_service=SERVICE)
service_ekyc = ServiceEKYC()
service_gw = ServiceGW()
service_idm = ServiceIDM()
service_kafka = ServiceKafka()
service_redis = ServiceRedis()



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

    return stop_app
