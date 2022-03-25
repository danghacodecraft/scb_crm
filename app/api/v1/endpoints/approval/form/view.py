from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.form.controller import (
    CtrApprovalFormResponse
)
from app.api.v1.endpoints.approval.form.schema import ApprovalFormResponse

router = APIRouter()


@router.get(
    path="/form/",
    name="Biểu Mẫu",
    description="Lấy biểu mẫu",
    responses=swagger_response(
        response_model=ResponseData[List[ApprovalFormResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fingers(
        current_user=Depends(get_current_user_from_header())
):
    fingers_info = await CtrApprovalFormResponse(current_user).ctr_get_approval_form()
    return ResponseData[List[ApprovalFormResponse]](**fingers_info)
