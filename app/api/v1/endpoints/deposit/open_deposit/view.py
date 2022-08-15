from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.schema import SaveCasaSuccessResponse
from app.api.v1.endpoints.deposit.open_deposit.controller import CtrDeposit
from app.api.v1.endpoints.deposit.open_deposit.schema import (
    DepositOpenTDAccountRequest, DepositPayInRequest, DepositPayInResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[DEPOSIT] Mở tài khoản tiết kiệm",
    description="[DEPOSIT] Mở tài khoản tiết kiệm",
    responses=swagger_response(
        response_model=ResponseData[SaveCasaSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_deposit_open_td_account(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),
        deposit_account_request: DepositOpenTDAccountRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    save_deposit_account = await CtrDeposit(current_user=current_user).ctr_save_deposit_open_td_account(
        BOOKING_ID=BOOKING_ID,
        deposit_account_request=deposit_account_request
    )
    return ResponseData(**save_deposit_account)


@router.post(
    path="/pay-in/",
    name="[DEPOSIT] Nguồn tiền",
    description="[DEPOSIT] Nguồn tiền",
    responses=swagger_response(
        response_model=ResponseData[SaveCasaSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_deposit_pay_in(
        booking_id: str = Header(..., description="Mã phiên giao dịch", alias="BOOKING-ID"),
        deposit_pay_in_request: DepositPayInRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    save_pay_in = await CtrDeposit(current_user=current_user).ctr_save_deposit_pay_in(
        booking_id=booking_id,
        deposit_pay_in_request=deposit_pay_in_request
    )
    return ResponseData[SaveCasaSuccessResponse](**save_pay_in)


@router.get(
    path="/pay-in/",
    name="[DEPOSIT] Nguồn tiền",
    description="[DEPOSIT] Nguồn tiền",
    responses=swagger_response(
        response_model=ResponseData[DepositPayInResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_deposit_pay_in(
        booking_id: str = Header(..., description="Mã phiên giao dịch", alias="BOOKING-ID"),
        current_user=Depends(get_current_user_from_header())
):
    get_pay_in = await CtrDeposit(current_user=current_user).ctr_get_deposit_pay_in(
        booking_id=booking_id
    )
    return ResponseData[DepositPayInResponse](**get_pay_in)
