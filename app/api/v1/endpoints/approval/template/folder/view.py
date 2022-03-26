from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.template.folder.controller import (
    CtrApprovalFormResponse
)
from app.api.v1.endpoints.approval.template.folder.schema import (
    ApprovalFormResponse
)

router = APIRouter()


@router.get(
    path="/folders/",
    name="Danh sách Biểu Mẫu",
    description="Lấy danh sách các biểu mẫu",
    responses=swagger_response(
        response_model=ResponseData[List[ApprovalFormResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_approval_template_info(
        cif_id=Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fingers_info = await CtrApprovalFormResponse(current_user).ctr_get_approval_template_info(cif_id=cif_id)
    return ResponseData[List[ApprovalFormResponse]](**fingers_info)
