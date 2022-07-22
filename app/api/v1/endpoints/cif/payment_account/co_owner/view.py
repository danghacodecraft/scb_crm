from typing import List

from fastapi import APIRouter, Depends, Header, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.payment_account.co_owner.controller import (
    CtrCoOwner
)
from app.api.v1.endpoints.cif.payment_account.co_owner.schema import (
    AccountHolderRequest, GetCoOwnerResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="B. Thông tin đồng sở hữu",
    description="Tạo dữ liệu tab `THÔNG TIN ĐỒNG SỞ HỮU` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_co_owner(
        co_owner: AccountHolderRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_save_co_owner(cif_id, co_owner, booking_id=BOOKING_ID)
    return ResponseData[SaveSuccessResponse](**co_owner_data)


@router.get(
    path="/list-co-owner",
    name="B. Danh Sách thông tin đồng sở hữu",
    description="Danh Sách thông tin đồng sở hữu",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_lits_retrieve_co_owner(
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_list_co_owner(cif_id=cif_id, booking_id=BOOKING_ID)
    return ResponseData(**co_owner_data)


@router.get(
    path="/co-owner/",
    name="B. Đồng sở hữu tài khoản theo số văn bản",
    description="Đồng sở hữu tài khoản theo số văn bản",
    responses=swagger_response(
        response_model=ResponseData[List[GetCoOwnerResponse]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_co_owner_info(
        document_no: str = Query(..., description="Số văn bản"),
        cif_id: str = Path(..., description='Id CIF ảo'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    co_owner_info = await CtrCoOwner(current_user).ctr_co_owner_info(
        cif_id=cif_id,
        document_no=document_no,
        booking_id=BOOKING_ID
    )
    return ResponseData[List[GetCoOwnerResponse]](**co_owner_info)
