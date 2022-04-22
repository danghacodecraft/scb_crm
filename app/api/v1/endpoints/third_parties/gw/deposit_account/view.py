from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWCasaAccountByCIFNumberRequest, GWCasaAccountByCIFNumberResponse
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.controller import (
    CtrGWDepositAccount
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.schema import (
    GWDepositAccountByCIFNumberResponse, GWDepositAccountTDResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Danh sách Tài khoản tiết kiệm theo số CIF",
    description="[GW] Tìm kiếm danh sách Tài khoản tiết kiệm theo số CIF",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountByCIFNumberResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_deposit_account_by_cif_number(
        request: GWCasaAccountByCIFNumberRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_deposit_account = await CtrGWDepositAccount(current_user).ctr_gw_get_deposit_account_by_cif_number(
        cif_number=request.cif_number
    )
    return ResponseData[GWDepositAccountByCIFNumberResponse](**gw_deposit_account)


@router.post(
    path="/{account_number}/",
    name="[Thông tin tài khoản] Chi tiết tài khoản tiết kiệm",
    description="Lấy chi tiết tài Khoản tiết kiệm theo số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_deposit_account_td(
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header())
):
    gw_deposit_account_td = await CtrGWDepositAccount(current_user).ctr_gw_get_deposit_account_td(
        account_number=account_number
    )
    return ResponseData[GWDepositAccountTDResponse](**gw_deposit_account_td)
