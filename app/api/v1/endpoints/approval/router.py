from fastapi import APIRouter

from app.api.v1.endpoints.approval.face import view as views_face_info
from app.api.v1.endpoints.approval.finger import view as views_finger_info

router_module = APIRouter()

# router của [Thông tin xác thực] -> Khuôn mặt
router_module.include_router(router=views_face_info.router, prefix="/{cif_id}")
router_module.include_router(router=views_finger_info.router, prefix="/{cif_id}")
