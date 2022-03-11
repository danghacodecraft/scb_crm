from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.controller import CtrCasa
from app.api.v1.endpoints.casa.schema import (
    SaveWithdrawRequest, WithdrawResponse
)

router = APIRouter()


@router.get(
    path="/{cif_id}/",
    name="[CASA]",
    description="Rút tiền từ tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[WithdrawResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    casa_info = await CtrCasa().ctr_casa_info(cif_id=cif_id)
    return ResponseData[WithdrawResponse](**casa_info)


@router.post(
    path="/{cif_id}/",
    name="[CASA]",
    description="Rút tiền từ tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[WithdrawResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        request: SaveWithdrawRequest = Body(..., description="abc"),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    casa_info = await CtrCasa().ctr_save_casa_info(
        cif_id=cif_id,
        request=request
    )
    return ResponseData[WithdrawResponse](**casa_info)
