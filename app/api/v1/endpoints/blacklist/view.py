from typing import List, Union

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.blacklist.controller import CtrBlackList
from app.api.v1.endpoints.blacklist.schema import (
    BlacklistResponse, BlacklistRequest
)
from app.api.base.schema import ResponseData

router = APIRouter()


@router.post(
    path='/',
    name="Thêm dữ liệu blacklist",
    description="Thêm dữ liệu blacklist",
    responses=swagger_response(
        response_model=ResponseData[BlacklistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def create_blacklist(
    blacklist_request :BlacklistRequest
):
    data = await CtrBlackList().ctr_create_blacklist(blacklist_request)
    return ResponseData[BlacklistRequest](**data)


@router.get(
    path='/',
    name="Xem dữ liệu blacklist",
    description="Xem dữ liệu blacklist",
    responses=swagger_response(
        response_model=ResponseData[BlacklistResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_blacklist(
        pagination_params: PaginationParams = Depends(),
        identity_id: str = Query(..., description='Giấy tờ định danh'),
        # cif_num: List[str] = Query(None, description='số cif'),
        # casa_account: List[str] = Query(None, description='Số tài khoản ngân hàng tại SCB'),
) :
    list_identity = identity_id.split(',')
    data_blacklist = await CtrBlackList(pagination_params=pagination_params).ctr_view_blacklist(
                                                   list_identity,
                                                   # cif_num,
                                                   # casa_account
                                                   )
    return ResponseData[List[BlacklistResponse]](**data_blacklist)