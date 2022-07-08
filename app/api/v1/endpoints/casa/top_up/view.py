from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.top_up.controller import CtrCasaTopUp
from app.api.v1.endpoints.casa.top_up.schema import (
    CasaTopUpRequest, CasaTopUpResponse
)

router = APIRouter()


@router.post(
    path="/top-up/",
    name="Nộp tiền",
    description="Nộp tiền",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_casa_top_up_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: CasaTopUpRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    casa_top_up_info = await CtrCasaTopUp(current_user).ctr_save_casa_top_up_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData(**casa_top_up_info)


@router.get(
    path="/top-up/",
    name="Nộp tiền",
    description="Nộp tiền",
    responses=swagger_response(
        response_model=ResponseData[CasaTopUpResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_casa_top_up_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):

    get_casa_top_up_info = await CtrCasaTopUp(current_user).ctr_get_casa_top_up_info(
        booking_id=BOOKING_ID
    )
    return ResponseData[CasaTopUpResponse](**get_casa_top_up_info)
