from fastapi import APIRouter

from app.api.v1.endpoints.tablet.mobile import view as views_tablet_mobile
from app.api.v1.endpoints.tablet.web import view as views_tablet_web

router = APIRouter()

router.include_router(router=views_tablet_mobile.router, tags=["[Tablet] Mobile"], prefix='/mobile')

router.include_router(router=views_tablet_web.router, tags=["[Tablet] Web"], prefix='/web')
