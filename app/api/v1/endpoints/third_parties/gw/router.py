from fastapi import APIRouter

from app.api.v1.endpoints.third_parties.gw.casa_account import \
    view as views_casa_account

router_module = APIRouter()

router_module.include_router(
    router=views_casa_account.router, prefix="/casa-account", tags=["[Third-Party][GW][Casa-Account]"]
)
