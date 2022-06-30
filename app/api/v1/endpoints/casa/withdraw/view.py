from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.withdraw.controller import CtrWithdraw
from app.api.v1.endpoints.casa.withdraw.schema import WithdrawRequest

router = APIRouter()


@router.post(
    path="/withdraw/",
    name="Rút tiền từ tài khoản thanh toán",
    description="Rút tiền từ tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_withdraw_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: WithdrawRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    casa_info = await CtrWithdraw(current_user).ctr_save_withdraw_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData(**casa_info)
