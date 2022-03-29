from fastapi import APIRouter

from app.api.v1.endpoints.user.profile.curriculum_vitae.contact_info import \
    view as views_contact_info
from app.api.v1.endpoints.user.profile.curriculum_vitae.personal_info import \
    view as views_personal_info

router_module = APIRouter()

# router [SƠ YẾU LÍ LỊCH] - A. THÔNG TIN CÁ NHÂN
router_module.include_router(router=views_personal_info.router, prefix="/personal-info")

# router [SƠ YẾU LÍ LỊCH] - B. THÔNG TIN LIÊN HỆ
router_module.include_router(router=views_contact_info.router, prefix="/contact-info")
