from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField


class TdAccountRequest(BaseSchema):
    pass


class DepositOpenTDAccountRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
    td_account: List[TdAccountRequest] = Field(..., description="Danh sách TKTK")
