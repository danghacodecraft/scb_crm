from fastapi import APIRouter

from app.api.v1.endpoints.third_parties.gw.branch_location import \
    view as views_branch_location
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
from app.api.v1.endpoints.third_parties.gw.payment import view as views_payment
from app.api.v1.endpoints.third_parties.gw.statistics import \
    view as views_statistic
from app.api.v1.endpoints.third_parties.gw.user import view as views_user

router_module = APIRouter()

router_module.include_router(router=views_casa_account.router, prefix="/casa-account", tags=["[Third-Party][GW][Casa-Account]"])

router_module.include_router(router=views_deposit_account.router, prefix="/deposit-account", tags=["[Third-Party][GW][Deposit-Account]"])

router_module.include_router(router=views_customer.router, prefix="/customer", tags=["[Third-Party][GW][Customer]"])

router_module.include_router(router=views_employee.router, prefix="/employee", tags=["[Third-Party][GW][Employee]"])

router_module.include_router(router=views_organization.router, prefix="/organization", tags=["[Third-Party][GW][Organization]"])

router_module.include_router(router=views_category.router, prefix="/category", tags=["[Third-Party][GW][Category]"])

router_module.include_router(router=views_history.router, prefix="/history", tags=["[Third-Party][GW][History]"])

router_module.include_router(router=views_payment.router, prefix="/payment", tags=["[Third-Party][GW][Payment]"])

router_module.include_router(router=views_user.router, prefix="/user", tags=["[Third-Party][GW][User]"])

router_module.include_router(router=views_branch_location.router, prefix="/branch-location", tags=["[Third-Party][GW][Branch-Location]"])

router_module.include_router(router=views_statistic.router, prefix="/statistic", tags=["[Third-Party][GW][Statistic]"])
