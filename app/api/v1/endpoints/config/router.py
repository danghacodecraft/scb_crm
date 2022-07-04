from fastapi import APIRouter

from app.api.v1.endpoints.config.account import view as views_account_info
from app.api.v1.endpoints.config.address import view as views_address_info
from app.api.v1.endpoints.config.approval import view as view_approval
from app.api.v1.endpoints.config.bank import view as views_bank_info
from app.api.v1.endpoints.config.branch import view as views_branch_info
from app.api.v1.endpoints.config.cif_information import view as views_cif_info
from app.api.v1.endpoints.config.currency import view as views_currency_info
from app.api.v1.endpoints.config.customer import view as views_customer_info
from app.api.v1.endpoints.config.customer.contact_type import \
    view as view_contact_type_info
from app.api.v1.endpoints.config.dashboard import view as view_dashboard
from app.api.v1.endpoints.config.debit_card import view as view_debit_card_info
from app.api.v1.endpoints.config.deposit import view as view_deposit
from app.api.v1.endpoints.config.e_banking import view as view_e_banking_info
from app.api.v1.endpoints.config.fatca import view as view_fatca_info
from app.api.v1.endpoints.config.gis.area import view as view_area
from app.api.v1.endpoints.config.gis.branch import view as view_branch
from app.api.v1.endpoints.config.gis.branchgeojson import \
    view as view_branchgeojson
from app.api.v1.endpoints.config.gis.region import view as view_region
from app.api.v1.endpoints.config.hand import view as views_hand_info
from app.api.v1.endpoints.config.identity_document import \
    view as views_identity_document_type_info
from app.api.v1.endpoints.config.passport import view as views_passport_info
from app.api.v1.endpoints.config.payment_account.co_owner import \
    view as view_co_owner_info
from app.api.v1.endpoints.config.payment_account.detail import \
    view as view_payment_detail_info
from app.api.v1.endpoints.config.personal import view as views_personal_info
from app.api.v1.endpoints.config.post_check import view as view_post_check
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

router.include_router(router=view_debit_card_info.router)

router.include_router(router=view_co_owner_info.router)

router.include_router(router=view_payment_detail_info.router)

router.include_router(router=view_contact_type_info.router)

router.include_router(router=view_post_check.router)

router.include_router(router=view_approval.router, prefix="/approval")

router.include_router(router=view_region.router)

router.include_router(router=view_area.router)

router.include_router(router=view_branch.router)

router.include_router(router=view_branchgeojson.router)

router.include_router(router=view_dashboard.router)

router.include_router(router=view_deposit.router)

router.include_router(router=views_bank_info.router, prefix="/bank")
