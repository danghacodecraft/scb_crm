from fastapi import APIRouter

from app.api.v1.endpoints.user.profile.others.discipline import \
    view as views_discipline
from app.api.v1.endpoints.user.profile.others.felicitation import \
    view as views_felicitation
from app.api.v1.endpoints.user.profile.others.sub_info import \
    view as views_sub_info
from app.api.v1.endpoints.user.profile.others.training_in_scb import \
    view as views_training_in_scb

router_module = APIRouter()

# router [THÔNG TIN KHÁC] - A. KHEN THƯỞNG
router_module.include_router(router=views_felicitation.router, prefix="/felicitation")

# router [THÔNG TIN KHÁC] - B. KỶ LUẬT
router_module.include_router(router=views_discipline.router, prefix="/discipline")

# router [THÔNG TIN KHÁC] - C. ĐÀO TẠO TRONG NH
router_module.include_router(router=views_training_in_scb.router, prefix="/training-in-scb")

# router [THÔNG TIN KHÁC] - D. THÔNG TIN PHỤ
router_module.include_router(router=views_sub_info.router, prefix="/sub-info")
