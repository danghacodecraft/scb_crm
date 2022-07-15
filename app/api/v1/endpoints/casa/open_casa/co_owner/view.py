from typing import List

from fastapi import APIRouter, Depends, Header, Path, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.open_casa.co_owner.controller import CtrCoOwner
from app.api.v1.endpoints.casa.open_casa.co_owner.schema import (
    AccountHolderRequest, CoOwnerRequest, GetCoOwnerResponse,
    ListCoOwnerResponse
)

router = APIRouter()


@router.post(
    path="/{account_id}/co-owner/",
    name="Đồng sở hữu tài khoản",
    description="Đồng sở hữu tài khoản",
    responses=swagger_response(
        response_model=ResponseData[CoOwnerRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_co_owner(
        co_owner: AccountHolderRequest,
        account_id: str = Path(..., description='Mã tài khoản thanh toán'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    co_owner_data = await CtrCoOwner(current_user).ctr_save_co_owner(account_id, co_owner, booking_id=BOOKING_ID)
    return ResponseData[CoOwnerRequest](**co_owner_data)


@router.get(
    path="/{account_id}/list-co-owner",
    name="Danh sách thông tin đồng sở hữu",
    description="Danh sách thông tin đồng sở hữu",
    responses=swagger_response(
        response_model=ResponseData[List[ListCoOwnerResponse]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_co_owner(
        account_id: str = Path(..., description='Mã tài khoản thanh toán'),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    list_co_owner_data = await CtrCoOwner(current_user).ctr_get_co_owner(account_id, booking_id=BOOKING_ID)
    return ResponseData[List[ListCoOwnerResponse]](**list_co_owner_data)


@router.get(
    path="/co-owner",
    name="Danh sách đồng sở hữu tài khoản theo số văn bản",
    description="Danh sách đồng sở hữu tài khoản theo số văn bản",
    responses=swagger_response(
        response_model=ResponseData[List[GetCoOwnerResponse]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_co_owner_info(
        document_no: str = Query(..., description="Số văn bản"),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    co_owner_info = await CtrCoOwner(current_user).ctr_co_owner_info(document_no, booking_id=BOOKING_ID)
    return ResponseData[List[GetCoOwnerResponse]](**co_owner_info)
