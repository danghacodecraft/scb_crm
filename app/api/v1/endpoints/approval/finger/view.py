from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.finger.controller import CtrFingers
from app.api.v1.endpoints.approval.finger.schema import (
    CompareFingerPrintRequest, CompareFingerPrintResponse, FingersResponse
)

router = APIRouter()


@router.get(
    path="/finger/",
    name="Lấy hình vân tay",
    description="Lấy hình vân tay",
    responses=swagger_response(
        response_model=ResponseData[FingersResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fingers(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fingers_info = await CtrFingers(current_user).ctr_get_fingerprint(cif_id)
    return ResponseData[FingersResponse](**fingers_info)


@router.post(
    path="/finger/",
    name="1. GTĐD - C. Vân tay - So Sánh",
    description="Tìm kiếm vân tay có trong hệ thống",
    responses=swagger_response(
        response_model=ResponseData[List[CompareFingerPrintResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_compare_fingerprint(
        uuid: CompareFingerPrintRequest,
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    compare_fingerprint = await CtrFingers(current_user).ctr_compare_fingerprint(cif_id=cif_id, uuid=uuid)
    return ResponseData[List[CompareFingerPrintResponse]](**compare_fingerprint)
