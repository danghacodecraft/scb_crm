from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class GWCategoryRequest(BaseSchema):
    transaction_name: str = Field(...)
    transaction_value: List = Field([])
