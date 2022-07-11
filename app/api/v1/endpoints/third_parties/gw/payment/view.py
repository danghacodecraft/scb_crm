from typing import List

from fastapi import APIRouter, Body, Depends, Header
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
    AccountAmountUnblockRequest, PaymentSuccessResponse, RedeemAccountRequest
)

router = APIRouter()


@router.post(
    path="/amount-block/",
    name="Amount Block",
    description="Phong tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[PaymentSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_amount_block(
        account_amount_blocks: List[AccountAmountBlockRequest] = Body(...),
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    payment_amount_block = await CtrGWPayment(current_user).ctr_payment_amount_block(
        BOOKING_ID=BOOKING_ID,
        account_amount_blocks=account_amount_blocks
    )

    return ResponseData[PaymentSuccessResponse](**payment_amount_block)


@router.post(
    path="/amount-block-pd/",
    name="[GW] Amount Block",
    description="Phong tỏa tài khoản - Phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[AccountAmountBlockResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_block(
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    gw_payment_amount_block = await CtrGWPayment(current_user).ctr_gw_payment_amount_block(
        BOOKING_ID=BOOKING_ID
    )

    return ResponseData[AccountAmountBlockResponse](**gw_payment_amount_block)


@router.post(
    path="/amount-unblock/",
    name="Amount Unblock",
    description="Giải tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[PaymentSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_amount_unblock(
        account_amount_unblocks: List[AccountAmountUnblockRequest] = Body(...),
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    payment_amount_unblock = await CtrGWPayment(current_user).ctr_payment_amount_unblock(
        account_amount_unblocks=account_amount_unblocks,
        BOOKING_ID=BOOKING_ID
    )

    return ResponseData[PaymentSuccessResponse](**payment_amount_unblock)


@router.post(
    path="/amount-unblock-pd/",
    name="[GW] Amount Unblock",
    description="Giải tỏa tài khoản - Phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[AccountAmountBlockResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_amount_unblock_pd(
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    payment_amount_unblock_pd = await CtrGWPayment(current_user).ctr_gw_payment_amount_unblock(
        BOOKING_ID=BOOKING_ID
    )

    return ResponseData[AccountAmountBlockResponse](**payment_amount_unblock_pd)


# @router.post(
#     path="/pay-in-cash/",
#     name="[GW] Pay In Cash",
#     description="Nộp tiền mặt vô tài khoản thanh toán",
#     responses=swagger_response(
#         response_model=ResponseData[AccountAmountUnblock],
#         success_status_code=status.HTTP_200_OK
#     )
# )
# async def gw_pay_in_cash(
#         pay_in_cash: PayInCashRequest = Body(...),
#         current_user=Depends(get_current_user_from_header())
# ):
#     pay_in_cash = await CtrGWPayment(current_user).ctr_gw_pay_in_cash(pay_in_cash=pay_in_cash)
#     return ResponseData(**pay_in_cash)


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


@router.post(
    path="/transfer-pd/",
    name="[GW] Chuyển khoản",
    description="Chuyển khoản - Phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[PaymentSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_casa_transfer_pd(
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    casa_transfer_pd = await CtrGWPayment(current_user).ctr_gw_save_casa_transfer_info(
        BOOKING_ID=BOOKING_ID
    )

    return ResponseData[PaymentSuccessResponse](**casa_transfer_pd)
