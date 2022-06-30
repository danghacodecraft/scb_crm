from fastapi import APIRouter

from app.api.v1.endpoints.casa.close_casa import view as view_close_casa
from app.api.v1.endpoints.casa.open_casa import router as routers_open_casa
from app.api.v1.endpoints.casa.pay_in_cash import view as views_pay_in_cash
from app.api.v1.endpoints.casa.withdraw import view as views_withdraw_info

router_module = APIRouter()

# router của thông tin Casa -> Rút tiền

router_module.include_router(router=views_withdraw_info.router)

# router của thông tin Casa -> Mở tài khoản

router_module.include_router(router=routers_open_casa.router_module)

# router của thông tin Casa -> Đóng tài khoản

router_module.include_router(router=view_close_casa.router)

# router của thông tin Casa -> Nộp tiền mặt
router_module.include_router(router=views_pay_in_cash.router)
