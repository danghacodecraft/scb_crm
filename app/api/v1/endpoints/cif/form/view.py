from typing import List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.form.controller import CtrForm
from app.api.v1.endpoints.cif.form.schema import (
    CifApprovalProcessResponse, CifApprovalResponse,
    CifApprovalSuccessResponse, CifApproveRequest
)

router = APIRouter()


@router.get(
    path="/approval-process/",
    name="Approval process",
    description="Lấy dữ liệu tab `VI. PHÊ DUYỆT - QUÁ TRÌNH XỬ LÝ HỒ SƠ` ",
    responses=swagger_response(
        response_model=ResponseData[List[CifApprovalProcessResponse]],
        success_status_code=status.HTTP_200_OK
    ),
    deprecated=True
)
async def view_approval_process(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    approval_process = await CtrForm(current_user).ctr_approval_process(cif_id)
    return ResponseData[List[CifApprovalProcessResponse]](**approval_process)


@router.post(
    path="/approval/",
    description="Phê duyệt biểu mẫu",
    responses=swagger_response(
        response_model=ResponseData[CifApprovalResponse],
        success_status_code=status.HTTP_200_OK
    ),
    deprecated=True
)
async def view_approve(
        cif_id: str = Path(..., description='Id CIF ảo'),
        request: CifApproveRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrForm(current_user).ctr_approve(
        cif_id=cif_id,
        request=request
    )

    return ResponseData[CifApprovalResponse](**approve_info)


@router.get(
    path="/approval/",
    description="Phê duyệt biểu mẫu",
    responses=swagger_response(
        response_model=ResponseData[CifApprovalSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    deprecated=True
)
async def view_get_approve(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrForm(current_user).ctr_get_approval(
        cif_id=cif_id
    )

    return ResponseData[CifApprovalSuccessResponse](**approve_info)
