from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.dashboard.controller import CtrDashboard
from app.api.v1.endpoints.dashboard.schema import (
    CustomerInfoResponse, TransactionListResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="Transaction List",
    description="Danh sách giao dịch",
    responses=swagger_response(
        response_model=ResponseData[TransactionListResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_transaction_list(
        search_box: Optional[str] = None,
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends()
):
    transaction_list_response = await CtrDashboard(
        pagination_params=pagination_params
    ).ctr_get_transaction_list(search_box=search_box)
    return PagingResponse[TransactionListResponse](**transaction_list_response)


@router.get(
    path="/customer/",
    name="Danh sách khách hàng",
    description="Danh sách khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CustomerInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customers(
        cif_number: str = Query(None, description='Số cif'),
        identity_number: str = Query(None, description='Số giấy tờ định danh'),
        phone_number: str = Query(None, description='Số điện thoại'),
        full_name: str = Query(None, description='Họ và tên'),
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends()

):
    customers = await CtrDashboard(
        current_user,
        pagination_params=pagination_params
    ).ctr_get_customer_list(
        cif_number=cif_number,
        identity_number=identity_number,
        phone_number=phone_number,
        full_name=full_name
    )

    return PagingResponse[CustomerInfoResponse](**customers)
