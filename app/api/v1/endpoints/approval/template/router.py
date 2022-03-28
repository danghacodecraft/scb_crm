from fastapi import APIRouter

from app.api.v1.endpoints.approval.template.detail import \
    view as views_template_detail_info
from app.api.v1.endpoints.approval.template.folder import \
    view as views_template_folder_info

router_module = APIRouter()

# router của thông tin phê duyệt Danh sách biểu mẫu
router_module.include_router(router=views_template_folder_info.router, prefix="/template/folder")

# router của [Thông tin phê duyệt] Chi tiết biểu mẫu
router_module.include_router(router=views_template_detail_info.router, prefix="/template/detail")
