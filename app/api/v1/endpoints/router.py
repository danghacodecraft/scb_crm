from fastapi import APIRouter

from app.api.v1.endpoints.approval import router as routers_approval
from app.api.v1.endpoints.booking import view as view_bookings
from app.api.v1.endpoints.casa import router as routers_casa
from app.api.v1.endpoints.cif import router as routers_cif
from app.api.v1.endpoints.config import router as routers_config
from app.api.v1.endpoints.dashboard import router as routers_dashboard
from app.api.v1.endpoints.deposit import router as router_deposit
from app.api.v1.endpoints.document_file import view as view_document_file
from app.api.v1.endpoints.ekyc import view as view_ekyc
from app.api.v1.endpoints.file import view as views_file
from app.api.v1.endpoints.mobile import view as router_mobile
from app.api.v1.endpoints.news import view as view_scb_news
from app.api.v1.endpoints.post_check import view as view_post_check
from app.api.v1.endpoints.tablet import router as routers_tablet
from app.api.v1.endpoints.third_parties import router as router_third_party
from app.api.v1.endpoints.user import router as routers_user

router = APIRouter()

router.include_router(router=routers_tablet.router, prefix="/tablet")

router.include_router(router=routers_user.router_module, prefix="/users", tags=["User"])

router.include_router(router=views_file.router, prefix="/files", tags=["File"])

router.include_router(router=view_post_check.router, prefix="/post-check", tags=["KSS"])

router.include_router(router=routers_config.router, prefix="/config", tags=["Configs"])

router.include_router(router=view_bookings.router, prefix="/booking", tags=["[Booking]"])

router.include_router(router=view_document_file.router, prefix="/document", tags=["[Document]"])

router.include_router(router=routers_cif.router_module, prefix="/cif")

router.include_router(router=routers_user.router_module, prefix="/users")

router.include_router(router=routers_dashboard.router_module, prefix="/dashboard", tags=["Dashboard"])

router.include_router(router=routers_casa.router_module, prefix="/casa", tags=["[Casa] Information"])

router.include_router(router=routers_approval.router_module, prefix="/approval", tags=["[Approval] Information"])

router.include_router(router=view_scb_news.router, prefix="/news", tags=["[News]"])

router.include_router(router=router_third_party.router_module, prefix="/third-party")

router.include_router(router=router_mobile.router, prefix="/mobile", tags=["[Mobile]"])

router.include_router(router=router_deposit.router_module, prefix="/deposit", tags=["[Deposit]"])

router.include_router(router=view_ekyc.router, prefix="/ekyc", tags=["[eKYC]"])
