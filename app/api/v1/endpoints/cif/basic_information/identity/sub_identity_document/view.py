from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.controller import (
    CtrSubIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.sub_identity_document.schema import (
    LogResponse, SubIdentityDetailResponse, SubIdentityDocumentRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - E. GTĐD phụ - Lưu",
    description="Lưu lại I. TTCN - Giấy tờ định danh - E. Giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save(
        sub_identity_request: List[SubIdentityDocumentRequest],
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    save_info = await CtrSubIdentityDocument(current_user).save_sub_identity(
        sub_identity_request=sub_identity_request,
        cif_id=cif_id
    )
    return ResponseData[SaveSuccessResponse](**save_info)


@router.get(
    path="/",
    name="1. GTĐD - E. GTĐD phụ - Chi tiết",
    description="Chi tiết I. TTCN - Giấy tờ định danh - E. Giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[List[SubIdentityDetailResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_sub_identity_document = CtrSubIdentityDocument(current_user)

    detail_info = await ctr_sub_identity_document.get_detail_sub_identity(
        cif_id=cif_id
    )
    return ResponseData[List[SubIdentityDetailResponse]](**detail_info)


@router.get(
    path="/log/",
    name="1. GTĐD - E. GTĐD phụ - Lịch sử",
    description="Lịch sử thay đổi giấy tờ định danh phụ",
    responses=swagger_response(
        response_model=ResponseData[List[LogResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_logs(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_sub_identity_document = CtrSubIdentityDocument(current_user)

    logs_info = await ctr_sub_identity_document.get_sub_identity_log_list(
        cif_id=cif_id
    )
    return ResponseData[List[LogResponse]](**logs_info)
