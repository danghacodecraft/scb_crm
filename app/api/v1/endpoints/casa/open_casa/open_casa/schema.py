from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.cif.payment_account.detail.schema import SavePaymentAccountRequest


class CasaOpenCasaRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    save_payment_account_requests: List[SavePaymentAccountRequest] = Field(..., description="Danh sách TKTT")
