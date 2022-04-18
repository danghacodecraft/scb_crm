from typing import List

from fastapi import APIRouter, Depends, File, Path, UploadFile
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.signature.controller import CtrSignature
from app.api.v1.endpoints.approval.signature.schema import (
    CompareSignatureResponse
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
        signature_img: UploadFile = File(..., description="Hình ảnh chữ ký"),
        cif_id: str = Path(..., description="cif_id"),
        current_user=Depends(get_current_user_from_header())
):
    signature = await CtrSignature(current_user).ctr_compare_signature(cif_id=cif_id, signature_img=signature_img)
    return ResponseData[List[CompareSignatureResponse]](**signature)
