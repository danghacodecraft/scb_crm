from fastapi import APIRouter

from app.api.v1.endpoints.casa.withdraw import view as views_withdraw_info

router_module = APIRouter()

# router của thông tin Casa -> Rút tiền

router_module.include_router(router=views_withdraw_info.router)
