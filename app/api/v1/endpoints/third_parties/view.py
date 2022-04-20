from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.controller import CtrGW
from app.api.v1.endpoints.third_parties.schema import (
    GWCasaAccountByCIFNumberRequest, GWCasaAccountByCIFNumberResponse
)

router = APIRouter()


@router.post(
    path="/casa-account/",
    name="[GW] Danh sách Tài Khoản thanh toán theo số CIF",
    description="[GW] Tìm kiếm danh sách Tài Khoản thanh toán theo số CIF",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountByCIFNumberResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_casa_account_by_cif_number(
        request: GWCasaAccountByCIFNumberRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrGW(current_user).ctr_gw_get_casa_account_by_cif_number(
        cif_number=request.cif_number
    )
    return ResponseData[GWCasaAccountByCIFNumberResponse](**customer_information)
