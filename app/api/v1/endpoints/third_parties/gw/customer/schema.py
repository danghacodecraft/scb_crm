from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField


class CustomerInfoCIFResponse(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class CustomerInfoListCIFRequest(BaseSchema):
    cif_number: Optional[str] = CustomField().OptionalCIFNumberField


class GWCustomerCheckExistResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCustomerCheckExistRequest(BaseSchema):
    cif_number: str = CustomField().CIFNumberField
