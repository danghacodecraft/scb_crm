from fastapi import APIRouter

from app.api.v1.endpoints.config.account import view as views_account_info
from app.api.v1.endpoints.config.address import view as views_address_info
from app.api.v1.endpoints.config.branch import view as views_branch_info
from app.api.v1.endpoints.config.cif_information import view as views_cif_info
from app.api.v1.endpoints.config.currency import view as views_currency_info
from app.api.v1.endpoints.config.customer import view as views_customer_info
from app.api.v1.endpoints.config.e_banking import view as view_e_banking_info
from app.api.v1.endpoints.config.fatca import view as view_fatca_info
from app.api.v1.endpoints.config.hand import view as views_hand_info
from app.api.v1.endpoints.config.identity_document import \
    view as views_identity_document_type_info
from app.api.v1.endpoints.config.passport import view as views_passport_info
from app.api.v1.endpoints.config.personal import view as views_personal_info
from app.api.v1.endpoints.config.staff import view as views_staff_info

router = APIRouter()

router.include_router(router=views_hand_info.router)

router.include_router(router=views_cif_info.router)

router.include_router(router=views_address_info.router)

router.include_router(router=views_personal_info.router)

router.include_router(router=views_passport_info.router)

router.include_router(router=views_account_info.router)

router.include_router(router=views_currency_info.router)

router.include_router(router=views_staff_info.router)

router.include_router(router=views_customer_info.router)

router.include_router(router=views_identity_document_type_info.router)

router.include_router(router=views_branch_info.router)

router.include_router(router=view_fatca_info.router)

router.include_router(router=view_e_banking_info.router)
