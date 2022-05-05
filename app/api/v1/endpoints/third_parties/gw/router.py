from fastapi import APIRouter

from app.api.v1.endpoints.third_parties.gw.casa_account import \
    view as views_casa_account
from app.api.v1.endpoints.third_parties.gw.customer import \
    view as views_customer
from app.api.v1.endpoints.third_parties.gw.deposit_account import \
    view as views_deposit_account
from app.api.v1.endpoints.third_parties.gw.employee import \
    view as views_employee

router_module = APIRouter()

router_module.include_router(
    router=views_casa_account.router, prefix="/casa-account", tags=["[Third-Party][GW][Casa-Account]"]
)
router_module.include_router(
    router=views_deposit_account.router, prefix="/deposit-account", tags=["[Third-Party][GW][Deposit-Account]"]
)
router_module.include_router(
    router=views_customer.router, prefix="/customer", tags=["[Third-Party][GW][Customer]"]
)
router_module.include_router(
    router=views_employee.router, prefix="/employee", tags=["[Third-Party][GW][Employee]"]
)
