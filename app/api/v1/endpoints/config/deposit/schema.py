from pydantic import Field

from app.api.base.schema import BaseSchema


class AccClassRequest(BaseSchema):
    interest_type_id: str = Field(..., description="Hình thức lãi")
    currency_id: str = Field(..., description="Loại tiền")
    acc_type: str = Field(..., description="Sản phẩm")


class AccClassResponse(BaseSchema):
    ACCOUNT_CLASS: str = Field(...)
    DESCRIPTION: str = Field(...)
    SAN_PHAM_CAP_2: str = Field(...)
    SAN_PHAM_CAP_3: str = Field(...)
    KYHAN: str = Field(...)
    LAISUAT: str = Field(...)
    HINHTHUCLINHLAI: str = Field(...)
