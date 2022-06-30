from fastapi import APIRouter

from app.api.v1.endpoints.deposit.open_deposit import view as view_close_casa

router_module = APIRouter()

router_module.include_router(router=view_close_casa.router)
