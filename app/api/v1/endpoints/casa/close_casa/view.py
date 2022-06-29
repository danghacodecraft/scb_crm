from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.close_casa.controller import CtrCloseCasa
from app.api.v1.endpoints.casa.close_casa.schema import CloseCasaRequest

router = APIRouter()


@router.post(
    path="/close-casa/",
    name="Close Casa",
    description="Đóng tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    ),

)
async def view_close_casa(
        close_casa_request: CloseCasaRequest = Body(...),
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),
):
    redeem_account_response = await CtrCloseCasa(current_user).ctr_close_casa(
        booking_id=BOOKING_ID,
        close_casa_request=close_casa_request
    )
    return ResponseData(**redeem_account_response)
