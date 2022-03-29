from fastapi import APIRouter

from app.api.v1.endpoints.user.profile.work.decisive_contract import \
    view as views_decisive_contract
from app.api.v1.endpoints.user.profile.work.process import \
    view as views_work_process
from app.api.v1.endpoints.user.profile.work.work_profile import \
    view as views_work_profile_work_profile

router_module = APIRouter()

# router [HỒ SƠ CÔNG TÁC] - A. HỒ SƠ CÔNG TÁC
router_module.include_router(router=views_work_profile_work_profile.router)

# router [HỒ SƠ CÔNG TÁC] - B. QUYẾT ĐỊNH HỢP ĐỒNG
router_module.include_router(router=views_decisive_contract.router, prefix="/decisive-contract")

# router [HỒ SƠ CÔNG TÁC] - C. QUÁ TRÌNH CÔNG TÁC
router_module.include_router(router=views_work_process.router, prefix="/process")
