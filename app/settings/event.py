from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.third_parties.services.dwh import ServiceDWH
from app.third_parties.services.ekyc import ServiceEKYC
from app.third_parties.services.file import ServiceFile
from app.third_parties.services.gw import ServiceGW
from app.third_parties.services.idm import ServiceIDM
from app.third_parties.services.soa import ServiceSOA

service_file = ServiceFile()
service_ekyc = ServiceEKYC()
service_soa = ServiceSOA()
service_gw = ServiceGW()
service_idm = ServiceIDM()
service_dwh = ServiceDWH()



def create_start_app_handler(app: FastAPI) -> Callable:  # noqa
    async def start_app():
        service_file.start()
        service_ekyc.start()
        service_soa.start()
        service_gw.start()
        service_idm.start()
        service_dwh.start()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # noqa
    @logger.catch
    async def stop_app() -> None:
        await service_file.stop()
        await service_ekyc.stop()
        await service_soa.stop()
        await service_gw.stop()
        await service_dwh.stop()

    return stop_app
