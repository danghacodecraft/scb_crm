from fastapi import APIRouter

from app.api.v1.endpoints.third_parties.gw import router as routers_gw

router_module = APIRouter()

router_module.include_router(router=routers_gw.router_module, prefix="/gw")
