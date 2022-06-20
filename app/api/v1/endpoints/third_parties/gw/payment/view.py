from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.payment.controller import (
    CtrGWPayment
)
from app.api.v1.endpoints.third_parties.gw.payment.example import (
    REDEEM_ACCOUNT_REQUEST_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlockRequest, AccountAmountBlockResponse,
    AccountAmountUnblock, PayInCashRequest, PaymentSuccessResponse,
    RedeemAccountRequest
)

router = APIRouter()


@router.post(
    path="/{account_number}/amount-block/",
    name="[GW] Amount Block",
    description="Phong tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[AccountAmountBlockResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_block(
        account_amount_block: AccountAmountBlockRequest = Body(...),
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    gw_payment_amount_block = await CtrGWPayment(current_user).ctr_gw_payment_amount_block(
        BOOKING_ID=BOOKING_ID,
        account_number=account_number,
        account_amount_block=account_amount_block
    )

    return ResponseData(**gw_payment_amount_block)


@router.post(
    path="/amount-unblock/",
    name="[GW] Amount Unblock",
    description="Giải tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[PaymentSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_unblock(
        account_amount_unblock: AccountAmountUnblock = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_payment_amount_unblock = await CtrGWPayment(current_user).ctr_gw_payment_amount_unblock(
        account_amount_unblock=account_amount_unblock
    )
    return ResponseData[PaymentSuccessResponse](**gw_payment_amount_unblock)


@router.post(
    path="/pay-in-cash/",
    name="[GW] Pay In Cash",
    description="Nộp tiền mặt vô tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[AccountAmountUnblock],
        success_status_code=status.HTTP_200_OK
    )
)
async def gw_pay_in_cash(
        pay_in_cash: PayInCashRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    pay_in_cash = await CtrGWPayment(current_user).ctr_gw_pay_in_cash(pay_in_cash=pay_in_cash)
    return ResponseData(**pay_in_cash)


@router.post(
    path="/redeem-account/",
    name="[GW] Redeem Account",
    description="Tất toán sổ tiết kiệm",
    responses=swagger_response(
        response_model=ResponseData[PaymentSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),

)
async def gw_redeem_account(
        redeem_account: RedeemAccountRequest = Body(..., example=REDEEM_ACCOUNT_REQUEST_EXAMPLE),
        current_user=Depends(get_current_user_from_header())
):
    redeem_account_response = await CtrGWPayment(current_user).ctr_gw_redeem_account(redeem_account=redeem_account)
    return ResponseData[PaymentSuccessResponse](**redeem_account_response)
