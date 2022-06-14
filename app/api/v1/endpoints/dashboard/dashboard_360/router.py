from fastapi import APIRouter

from app.api.v1.endpoints.dashboard.dashboard_360.document_list import \
    view as view_document_list

router_module = APIRouter()

# router của thông tin Danh sách tài liệu
router_module.include_router(router=view_document_list.router, prefix="/360")
