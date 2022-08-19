from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.face.controller import CtrApproveFace
from app.api.v1.endpoints.approval_v2.face.schema import (
    ApprovalFaceRequest, ApprovalFaceSuccessResponse
)

router = APIRouter()


@router.post(
    path="/face/",
    description="[Thông tin xác thực] Upload khuôn mặt",
    name="So sánh khuôn mặt",
    responses=swagger_response(
        response_model=ResponseData[ApprovalFaceSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_face(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: ApprovalFaceRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproveFace(current_user).ctr_upload_face(
        request=request,
        booking_id=BOOKING_ID
    )

    return ResponseData[ApprovalFaceSuccessResponse](**approve_info)
