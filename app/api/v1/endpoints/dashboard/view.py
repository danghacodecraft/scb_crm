from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.dashboard.controller import CtrDashboard
from app.api.v1.endpoints.dashboard.schema import (
    AccountingEntryResponse, BranchResponse, CustomerInfoResponse,
    RegionResponse, TransactionListResponse
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
        region_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        transaction_type_id: Optional[str] = None,
        status_code: Optional[str] = None,
        search_box: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends(),
):
    transaction_list_response = await CtrDashboard(
        current_user=current_user,
        pagination_params=pagination_params,
    ).ctr_get_transaction_list(region_id=region_id, branch_id=branch_id, transaction_type_id=transaction_type_id,
                               status_code=status_code, search_box=search_box, from_date=from_date, to_date=to_date)

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


@router.get(
    path="/branch/",
    name="Branch",
    description="Chi nhánh",
    responses=swagger_response(
        response_model=ResponseData[BranchResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_branch(
        current_user=Depends(get_current_user_from_header())
):
    branch = await CtrDashboard(current_user).ctr_branch()
    return ResponseData[List[BranchResponse]](**branch)


@router.get(
    path="/accounting-entry/",
    name="Accounting entry",
    description="Tổng bút toán",
    responses=swagger_response(
        response_model=ResponseData[AccountingEntryResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_accounting_entry(
        current_user=Depends(get_current_user_from_header())
):
    accounting_entry = await CtrDashboard(current_user).ctr_accounting_entry()
    return ResponseData[List[AccountingEntryResponse]](**accounting_entry)


@router.get(
    path="/region/",
    name="Region",
    description="Vùng",
    responses=swagger_response(
        response_model=ResponseData[RegionResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_region(
        current_user=Depends(get_current_user_from_header())
):
    region = await CtrDashboard(current_user).ctr_region()
    return ResponseData[List[RegionResponse]](**region)
