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
    id_ekyc: int = Field(..., description='id ekyc')
    hand_side: DropdownRequest = Field(..., description='Loại bàn tay')
    finger_type: DropdownRequest = Field(..., description='Loại ngón tay')


class TwoFingerPrintRequest(BaseSchema):
    fingerprint_1: List[FingerPrintRequest] = Field(..., description='Mẫu vân tay 1')
    fingerprint_2: List[FingerPrintRequest] = Field(..., description='Mẫu vân tay 2')


class CompareFingerResponse(BaseSchema):
    id: int = Field(..., description='id image')
    accuracy: int = Field(..., description="Tỷ lệ phần trăm giống nhau")


class AddCompareFingerResponse(BaseSchema):
    image_url: str = Field(..., description='UUID serivce_file')
    id_ekyc: int = Field(..., description="ID ekyc")
    uuid_ekyc: str = Field(..., description="UUID ekyc")
    compare: List[CompareFingerResponse] = Field(None, description='Danh sách so sánh vân tay')
