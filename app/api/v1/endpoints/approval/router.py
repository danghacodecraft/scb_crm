from fastapi import APIRouter

from app.api.v1.endpoints.approval import view as views_approval_info
from app.api.v1.endpoints.approval.face import view as views_face_info
from app.api.v1.endpoints.approval.finger import view as views_finger_info
from app.api.v1.endpoints.approval.signature import view as views_step_i_1_d

router_module = APIRouter()

# router của thông tin phê duyệt
router_module.include_router(router=views_approval_info.router, prefix="/{cif_id}")

# router của [Thông tin xác thực] -> Khuôn mặt
router_module.include_router(router=views_face_info.router, prefix="/{cif_id}")
router_module.include_router(router=views_finger_info.router, prefix="/{cif_id}")
router_module.include_router(router=views_step_i_1_d.router, prefix="/{cif_id}")
