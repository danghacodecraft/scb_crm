from fastapi import APIRouter

from app.api.v1.endpoints.dashboard import view as views_dashboard_info
from app.api.v1.endpoints.dashboard.dashboard_360 import router as routers_360

router_module = APIRouter()

# router của thông tin Dashboard
router_module.include_router(router=views_dashboard_info.router)

# router của danh sách tài liệu
router_module.include_router(router=routers_360.router_module, prefix="",)
