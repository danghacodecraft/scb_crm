from pydantic import Field

from app.api.base.schema import BaseSchema


class CurrencyResponse(BaseSchema):
    currency_id: str = Field(..., description='Mã loại tiền tệ')
    currency_code: str = Field(..., description='Code loại tiền tệ')
    currency_name: str = Field(..., description='Tên loại tiền tệ')
    country_id: str = Field(..., description='Mã quốc gia')
    country_code: str = Field(..., description='Code quốc gia')
    country_name: str = Field(..., description='Tên quốc gia')
