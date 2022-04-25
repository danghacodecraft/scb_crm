from typing import Optional

from fastapi import Path
from pydantic import Field

from app.utils.constant.cif import (
    CIF_NUMBER_MAX_LENGTH, CIF_NUMBER_MIN_LENGTH, CIF_NUMBER_REGEX
)

STR_MIN_LENGTH = 1


class CustomField:
    def __init__(self, description: str = "Số CIF", min_length: Optional[int] = None, max_length: Optional[int] = None):
        """
        CIFNumberField: Field CIF Number với giá trị là bắt buộc nhập
        OptionalCIFNumberField: Field CIF Number với giá trị là không bắt buộc nhập
        CIFNumberPath: Path Parameter CIF Number
        """
        self.description = description
        self.min_length = min_length
        self.max_length = max_length

        self.CIFNumberField = Field(
            ..., description=self.description, min_length=CIF_NUMBER_MIN_LENGTH, max_length=CIF_NUMBER_MAX_LENGTH,
            regex=CIF_NUMBER_REGEX
        )
        self.OptionalCIFNumberField = Field(
            None, description=self.description, min_length=CIF_NUMBER_MIN_LENGTH, max_length=CIF_NUMBER_MAX_LENGTH,
            regex=CIF_NUMBER_REGEX
        )

        # Field này dùng khai báo Path Parameter
        self.CIFNumberPath = Path(
            ..., description="Số CIF", title="Số CIF", regex=CIF_NUMBER_REGEX, min_length=CIF_NUMBER_MIN_LENGTH,
            max_length=CIF_NUMBER_MAX_LENGTH
        )
