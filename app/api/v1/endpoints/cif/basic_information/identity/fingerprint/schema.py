from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import FingerPrintResponse
from app.api.v1.schemas.utils import DropdownRequest


class TwoFingerPrintResponse(BaseSchema):
    fingerprint_1: List[FingerPrintResponse] = Field(..., description='Mẫu vân tay 1')
    fingerprint_2: List[FingerPrintResponse] = Field(..., description='Mẫu vân tay 2')


class FingerPrintRequest(BaseSchema):
    image_url: str = Field(..., description='Ảnh bàn tay')
    uuid_ekyc: str = Field(..., description='uuid call ekyc')
    hand_side: DropdownRequest = Field(..., description='Loại bàn tay')
    finger_type: DropdownRequest = Field(..., description='Loại ngón tay')


class TwoFingerPrintRequest(BaseSchema):
    fingerprint_1: List[FingerPrintRequest] = Field(..., description='Mẫu vân tay 1')
    fingerprint_2: List[FingerPrintRequest] = Field(..., description='Mẫu vân tay 2')
