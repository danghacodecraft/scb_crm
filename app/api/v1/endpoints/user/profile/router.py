from fastapi import APIRouter

from app.api.v1.endpoints.user.profile import view as views_user_profile
from app.api.v1.endpoints.user.profile.cv import router as routers_cv
from app.api.v1.endpoints.user.profile.kpi import view as views_kpi
from app.api.v1.endpoints.user.profile.level import router as routers_level
from app.api.v1.endpoints.user.profile.other import router as routers_other
from app.api.v1.endpoints.user.profile.work import router as routers_work

router_module = APIRouter()

# router [THÔNG TIN CHI TIẾT NHÂN VIÊN]
router_module.include_router(router=views_user_profile.router, prefix="/profiles")

# router [HỒ SƠ CÔNG TÁC]
router_module.include_router(router=routers_work.router_module, prefix="/work")

# router [SƠ YẾU LÍ LỊCH]
router_module.include_router(router=routers_cv.router_module, prefix="/cv")

# router [THÔNG TIN TRÌNH ĐỘ]
router_module.include_router(router=routers_level.router_module, prefix="/level")

# router [THÔNG TIN KPIS]
router_module.include_router(router=views_kpi.router, prefix="/kpi")

# router [THÔNG TIN KHÁC]
router_module.include_router(router=routers_other.router_module, prefix="/other")
