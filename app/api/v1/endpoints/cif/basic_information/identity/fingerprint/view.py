from typing import List

from fastapi import APIRouter, Depends, File, Form, Header, Path, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.controller import (
    CtrFingerPrint
)
from app.api.v1.endpoints.cif.basic_information.identity.fingerprint.schema import (
    AddCompareFingerResponse, TwoFingerPrintRequest, TwoFingerPrintResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Lưu dữ liệu `MẪU VÂN TAY` của khách hàng",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_fingerprint(
        finger_request: TwoFingerPrintRequest,  # TODO: Thêm example
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    data = await CtrFingerPrint(current_user).ctr_save_fingerprint(cif_id, finger_request)
    return ResponseData[SaveSuccessResponse](**data)


@router.get(
    path="/",
    name="1. GTĐD - C. Vân tay",
    description="Lấy dữ liệu tab `VÂN TAY` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[TwoFingerPrintResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fingerprint(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fingerprint_info = await CtrFingerPrint(current_user).ctr_get_fingerprint(cif_id)
    return ResponseData[TwoFingerPrintResponse](**fingerprint_info)


@router.post(
    path="/add_compare/",
    name="1. GTĐD - C. Vân tay - so sánh vân tay",
    description="So sánh vân tay",
    responses=swagger_response(
        response_model=ResponseData[AddCompareFingerResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_add_fingerprint(
    file: UploadFile = File(..., description='file'),
    ids_finger: List[int] = Form(None, description="Truyền id_ekyc để so sánh với file upload"),
    BOOKING_ID: str = Header(None, description="Mã phiên giao dịch"),  # noqa
    cif_id: str = Path(...),
    current_user=Depends(get_current_user_from_header())
):
    add_finger = await CtrFingerPrint(current_user).ctr_add_fingerprint(
        cif_id=cif_id,
        file=file,
        ids_finger=ids_finger,
        booking_id=BOOKING_ID
    )
    return ResponseData[AddCompareFingerResponse](**add_finger)
