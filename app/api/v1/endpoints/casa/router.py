from fastapi import APIRouter

from app.api.v1.endpoints.casa import view as views_casa_info

router_module = APIRouter()

# router của thông tin cif
router_module.include_router(router=views_casa_info.router)
