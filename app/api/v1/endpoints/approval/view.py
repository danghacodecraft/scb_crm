from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Header
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.approval.controller import CtrApproval
from app.api.v1.endpoints.approval.schema import (
    ApprovalRequest, CifApprovalProcessResponse, CifApprovalResponse,
    CifApprovalSuccessResponse, ApprovalBusinessJob
)
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.functions import make_description_from_dict

router = APIRouter()
router_special = APIRouter()


@router.get(
    path="/job/",
    description="Tổng số nghiệp vụ hoàn thành",
    name="Tổng số nghiệp vụ hoàn thành",
    responses=swagger_response(
        response_model=ResponseData[List[ApprovalBusinessJob]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_business_jobs(
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        business_type_code: str = Query(
            ..., description=f"Mã loại nghiệp vụ {make_description_from_dict(dictionary=BUSINESS_TYPES)}"
        ),
        current_user=Depends(get_current_user_from_header())
):
    business_jobs = await CtrApproval(current_user).ctr_get_business_jobs(
        cif_id=cif_id,
        business_type_code=business_type_code,
        booking_id=BOOKING_ID
    )

    return ResponseData[List[ApprovalBusinessJob]](**business_jobs)


@router_special.get(
    path="/process/",
    name="Quá trình xử lý hồ sơ",
    description="Lấy dữ liệu tab `VI. PHÊ DUYỆT - QUÁ TRÌNH XỬ LÝ HỒ SƠ` ",
    responses=swagger_response(
        response_model=ResponseData[List[CifApprovalProcessResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_approval_process(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    approval_process = await CtrApproval(current_user).ctr_approval_process(booking_id=BOOKING_ID)
    return ResponseData[List[CifApprovalProcessResponse]](**approval_process)


@router.post(
    path="/",
    description="Phê duyệt - Phê duyệt biểu mẫu",
    name="Phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[CifApprovalResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_approve(
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: ApprovalRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproval(current_user).ctr_approve(
        cif_id=cif_id,
        booking_id=BOOKING_ID,
        request=request
    )

    return ResponseData[Optional[CifApprovalResponse]](**approve_info)


@router_special.get(
    path="/",
    description="Thông tin chi tiết - Phê duyệt biểu mẫu",
    name="Phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[CifApprovalSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_approve(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        amount: int = Query(2, description="Số lượng hình so sánh"),
        current_user=Depends(get_current_user_from_header())
):
    approve_info = await CtrApproval(current_user).ctr_get_approval(
        booking_id=BOOKING_ID,
        amount=amount
    )

    return ResponseData[CifApprovalSuccessResponse](**approve_info)


@router_special.get(
    path="/audit/",
    description="Thông tin KSS CIF",
    name="Kiểm soát sau CIF",
    responses=swagger_response(
        response_model=ResponseData[CifApprovalSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_list_audit(
        current_user=Depends(get_current_user_from_header())
):
    list_audit = await CtrApproval(current_user).ctr_get_list_audit()

    return PagingResponse(**list_audit)
