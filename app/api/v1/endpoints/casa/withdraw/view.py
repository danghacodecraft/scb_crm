from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.withdraw.controller import CtrWithdraw
from app.api.v1.endpoints.casa.withdraw.schema import (
    WithdrawRequest, WithdrawResponse
)

router = APIRouter()


@router.get(
    path="/{cif_id}/withdraw/",
    name="Withdraw",
    description="Rút tiền từ tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[WithdrawResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_withdraw_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    casa_info = await CtrWithdraw(current_user=current_user).ctr_withdraw_info(cif_id=cif_id)
    return ResponseData[WithdrawResponse](**casa_info)


@router.post(
    path="/{cif_id}/withdraw/",
    name="Withdraw",
    description="Rút tiền từ tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[WithdrawResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_withdraw_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),
        request: WithdrawRequest = Body(..., description="abc"),
        current_user=Depends(get_current_user_from_header())
):
    casa_info = await CtrWithdraw(current_user).ctr_save_withdraw_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData[WithdrawResponse](**casa_info)
