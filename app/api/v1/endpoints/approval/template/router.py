from fastapi import APIRouter

from app.api.v1.endpoints.approval.template.folder import \
    view as views_template_folder_info

router_module = APIRouter()

# router của thông tin phê duyệt
router_module.include_router(router=views_template_folder_info.router)
