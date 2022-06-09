from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.open_casa.open_casa.controller import (
    CtrCasaOpenCasa
)
from app.api.v1.endpoints.casa.open_casa.open_casa.schema import CasaOpenCasaRequest, CasaOpenCasaResponse
from app.api.v1.endpoints.casa.schema import SaveCasaSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="[CASA] Mở tài khoản thanh toán",
    description="[CASA] Mở tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[SaveCasaSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_casa_open_casa_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        open_casa_request: CasaOpenCasaRequest = Body(...),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    save_casa_open_casa_info = await CtrCasaOpenCasa(current_user=current_user).ctr_save_casa_open_casa_info(
        booking_parent_id=BOOKING_ID,
        cif_number=open_casa_request.cif_number,
        requests=open_casa_request.save_payment_account_requests
    )
    return ResponseData[SaveCasaSuccessResponse](**save_casa_open_casa_info)


@router.get(
    path="/",
    name="[CASA] Mở tài khoản thanh toán",
    description="[CASA] Mở tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_casa_open_casa_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())  # noqa
):
    get_casa_open_casa_info = await CtrCasaOpenCasa(current_user=current_user).ctr_get_casa_open_casa_info(
        booking_parent_id=BOOKING_ID
    )
    # return ResponseData(**get_casa_open_casa_info)
    return ResponseData[CasaOpenCasaResponse](**get_casa_open_casa_info)
