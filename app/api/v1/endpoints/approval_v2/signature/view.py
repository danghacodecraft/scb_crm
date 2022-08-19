from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval_v2.signature.controller import (
    CtrApproveSignature
)
from app.api.v1.endpoints.approval_v2.signature.schema import (
    ApprovalSignatureRequest, ApprovalSignatureSuccessResponse
)

router = APIRouter()


@router.post(
    path="/signature/",
    description="[Thông tin xác thực] Upload chữ ký",
    name="So sánh chữ ký",
    responses=swagger_response(
        response_model=ResponseData[ApprovalSignatureSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_signature(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: ApprovalSignatureRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproveSignature(current_user).ctr_upload_signature(
        request=request,
        booking_id=BOOKING_ID
    )

    return ResponseData[ApprovalSignatureSuccessResponse](**approve_info)
