from pydantic import Field

from app.api.base.schema import BaseSchema


class CurrencyDenominationResponse(BaseSchema):
    denominations_name: str = Field(..., description='Tên mệnh giá')
    denominations: str = Field(..., description='Mệnh giá')
