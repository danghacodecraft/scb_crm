from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.endpoints.cif.base_field import CustomField


class CustomerInfoCIFResponse(BaseSchema):
    cif_number: str = CustomField().CIFNumberField


class GWCustomerCheckExistResponse(BaseSchema):
    is_existed: bool = Field(..., description="Cờ có tồn tại không")


class GWCustomerCheckExistRequest(BaseSchema):
    cif_number: str = Field(..., description="Số tài khoản")
