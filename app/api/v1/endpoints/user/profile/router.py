from fastapi import APIRouter

from app.api.v1.endpoints.user.profile import view as views_user_profile
from app.api.v1.endpoints.user.profile.curriculum_vitae import \
    router as routers_curriculum_vitae
from app.api.v1.endpoints.user.profile.kpis import view as views_kpis
from app.api.v1.endpoints.user.profile.others import router as routers_others
from app.api.v1.endpoints.user.profile.qualification import \
    router as routers_qualification
from app.api.v1.endpoints.user.profile.work_profile import \
    router as routers_work_profile

router_module = APIRouter()

# router [THÔNG TIN CHI TIẾT NHÂN VIÊN]
router_module.include_router(router=views_user_profile.router)

# router [HỒ SƠ CÔNG TÁC]
router_module.include_router(router=routers_work_profile.router_module, prefix="/work-profile")

# router [SƠ YẾU LÍ LỊCH]
router_module.include_router(router=routers_curriculum_vitae.router_module, prefix="/curriculum-vitae")

# router [THÔNG TIN TRÌNH ĐỘ]
router_module.include_router(router=routers_qualification.router_module, prefix="/qualification")

# router [THÔNG TIN KPIS]
router_module.include_router(router=views_kpis.router, prefix="/kpis")

# router [THÔNG TIN KHÁC]
router_module.include_router(router=routers_others.router_module, prefix="/others")
