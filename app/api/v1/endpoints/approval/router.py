from fastapi import APIRouter

from app.api.v1.endpoints.approval import view as views_approval_info
from app.api.v1.endpoints.approval.face import view as views_face_info
from app.api.v1.endpoints.approval.finger import view as views_finger_info
from app.api.v1.endpoints.approval.form import view as views_form_info

router_module = APIRouter()

# router của thông tin phê duyệt
router_module.include_router(router=views_approval_info.router, prefix="/{cif_id}")

# router của [Thông tin xác thực] -> Khuôn mặt
router_module.include_router(router=views_face_info.router, prefix="/{cif_id}")

# router của [Thông tin xác thực] -> Vân tay
router_module.include_router(router=views_finger_info.router, prefix="/{cif_id}")

# router của [Thông tin xác thực] -> Biểu mẫu
router_module.include_router(router=views_form_info.router, prefix="/{cif_id}")
