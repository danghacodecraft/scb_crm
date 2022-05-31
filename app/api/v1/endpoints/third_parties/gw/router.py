from fastapi import APIRouter

from app.api.v1.endpoints.third_parties.gw.casa_account import \
    view as views_casa_account
from app.api.v1.endpoints.third_parties.gw.category import \
    view as views_category
from app.api.v1.endpoints.third_parties.gw.customer import \
    view as views_customer
from app.api.v1.endpoints.third_parties.gw.deposit_account import \
    view as views_deposit_account
from app.api.v1.endpoints.third_parties.gw.employee import \
    view as views_employee
from app.api.v1.endpoints.third_parties.gw.history import view as views_history
from app.api.v1.endpoints.third_parties.gw.organization import \
    view as views_organization

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
router_module.include_router(
    router=views_organization.router, prefix="/organization", tags=["[Third-Party][GW][Organization]"]
)
router_module.include_router(
    router=views_category.router, prefix="/category", tags=["[Third-Party][GW][Category]"]
)
router_module.include_router(
    router=views_history.router, prefix="/history", tags=["[Third-Party][GW][History]"]
)
