from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.cif.payment_account.detail.schema import SavePaymentAccountRequest, PaymentAccountResponse


class CasaOpenCasaRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    casa_accounts: List[SavePaymentAccountRequest] = Field(..., description="Danh sách TKTT")


class CasaOpenCasaResponse(BaseSchema):
    transaction_code: str = Field(..., description="Mã giao dịch")
    total_item: int = Field(..., description="Tổng số TKTT")
    casa_accounts: List[PaymentAccountResponse] = Field(..., description="Danh sách TKTT")

