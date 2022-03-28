from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.signature.controller import CtrSignature
from app.api.v1.endpoints.approval.signature.schema import (
    CompareSignatureRequest, CompareSignatureResponse
)

router = APIRouter()


@router.post(
    path="/signature/",
    name="So sánh chữ ký",
    description="Compare signature",
    responses=swagger_response(
        response_model=ResponseData[List[CompareSignatureResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_compare_signature(
    uuid_ekyc: CompareSignatureRequest,
    cif_id: str = Path(...),
    current_user=Depends(get_current_user_from_header())
):
    compare_signature = await CtrSignature(current_user).ctr_compare_signature(cif_id=cif_id, uuid_ekyc=uuid_ekyc)
    return ResponseData[List[CompareSignatureResponse]](**compare_signature)
