from pydantic import Field

from app.api.base.schema import BaseSchema


class SerialRequest(BaseSchema):
    account_class: str = Field(..., description="Mã sản phẩm")


class AccClassRequest(BaseSchema):
    interest_type_id: str = Field(..., description="Hình thức lãi")
    currency_id: str = Field(..., description="Loại tiền")
    acc_type: str = Field(..., description="Sản phẩm")


class AccClassResponse(BaseSchema):
    ACCOUNT_CLASS: str = Field(..., description="Mã sản phẩm")
    DESCRIPTION: str = Field(...)
    SAN_PHAM_CAP_2: str = Field(...)
    SAN_PHAM_CAP_3: str = Field(...)
    KYHAN: str = Field(...)
    LAISUAT: str = Field(...)
    HINHTHUCLINHLAI: str = Field(...)


class SerialResponse(BaseSchema):
    serial_org_id: str = Field(..., description="Mã ORG")
    serial_inventory_id: str = Field(..., description="Mã kiểm kê")
    serial_item_id: str = Field(..., description="Mã item")
    serial_receive_tran_id: str = Field(..., description="Mã giao dịch")
    serial_number: str = Field(..., description="Số seri")
    serial_prefix: str = Field(..., description="Số ký hiệu")
