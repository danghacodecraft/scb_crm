from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.fingerprint.controller import (
    CtrApproveFingerprint
)
from app.api.v1.endpoints.approval_v2.fingerprint.schema import (
    ApprovalFingerprintRequest, ApprovalFingerprintSuccessResponse
)

router = APIRouter()


@router.post(
    path="/fingerprint/",
    description="[Thông tin xác thực] Upload vân tay",
    name="So sánh vân tay",
    responses=swagger_response(
        response_model=ResponseData[ApprovalFingerprintSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_fingerprint(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: ApprovalFingerprintRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproveFingerprint(current_user).ctr_upload_fingerprint(
        request=request,
        booking_id=BOOKING_ID
    )

    return ResponseData[ApprovalFingerprintSuccessResponse](**approve_info)
