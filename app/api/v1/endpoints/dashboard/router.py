from fastapi import APIRouter

from app.api.v1.endpoints.dashboard import view as views_dashboard_info
from app.api.v1.endpoints.dashboard.account_info import \
    view as views_account_info

router_module = APIRouter()

# router của thông tin Dashboard
router_module.include_router(router=views_dashboard_info.router)
router_module.include_router(router=views_account_info.router, prefix="/account-info")
