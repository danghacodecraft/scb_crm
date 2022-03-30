from fastapi import APIRouter

from app.api.v1.endpoints.user.profile.level.education import \
    view as views_education
from app.api.v1.endpoints.user.profile.level.foreign import \
    view as views_foreign
from app.api.v1.endpoints.user.profile.level.it import view as views_it

router_module = APIRouter()

# router [THÔNG TIN TRÌNH ĐỘ] - A. TRÌNH ĐỘ VĂN HÓA
router_module.include_router(router=views_education.router, prefix="/education")

# router [THÔNG TIN TRÌNH ĐỘ] - B. TRÌNH ĐỘ NGOẠI NGỮ
router_module.include_router(router=views_foreign.router, prefix="/foreign")

# router [THÔNG TIN TRÌNH ĐỘ] - C. TRÌNH ĐỘ TIN HỌC
router_module.include_router(router=views_it.router, prefix="/it")
