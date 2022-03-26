from fastapi import APIRouter

from app.api.v1.endpoints.cif import view as views_cif_info
from app.api.v1.endpoints.cif.basic_information import router as routers_step_1
from app.api.v1.endpoints.cif.basic_information.identity.identity_document import \
    view as views_step_i_1_a
from app.api.v1.endpoints.cif.debit_card import view as views_debit_card
from app.api.v1.endpoints.cif.e_banking import view as views_e_banking
from app.api.v1.endpoints.cif.other_information import view as views_other_info
from app.api.v1.endpoints.cif.payment_account import \
    router as routers_payment_account

router_module = APIRouter()

# router của thông tin cif
router_module.include_router(router=views_cif_info.router, tags=["[CIF] Information"])

# step I. Thông tin cá nhân
router_module.include_router(router=routers_step_1.router_step, prefix="/{cif_id}/basic-information",
                             tags=['[CIF] I. TTCN'])

# router đặc biệt, do không sử dụng prefix có path param là {cif_id}
router_module.include_router(router=views_step_i_1_a.router_special, prefix="")

# step II. Thông tin khác
router_module.include_router(router=views_other_info.router, prefix="/{cif_id}/other-information",
                             tags=['[CIF] II. TTK'])

# step III. Tài khoản thanh toán
router_module.include_router(router=routers_payment_account.router_step, prefix="/{cif_id}/payment-account",
                             tags=['[CIF] III. TKTT'])

# step IV. E-banking
router_module.include_router(router=views_e_banking.router, prefix="/{cif_id}/e-banking",
                             tags=['[CIF] IV. E-banking'])

# step V. Thẻ ghi nợ
router_module.include_router(router=views_debit_card.router, prefix="/{cif_id}/debit-card",
                             tags=['[CIF] V. Thẻ ghi nợ'])
