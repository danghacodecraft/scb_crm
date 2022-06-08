from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.payment.controller import (
    CtrGWPayment
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    AccountAmountBlock
)

router = APIRouter()


@router.post(
    path="/{account_number}/amount-block/",
    name="[GW] Amount Block",
    description="Phong tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[AccountAmountBlock],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_block(
        account_amount_block: AccountAmountBlock = Body(...),
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header())
):

    gw_payment_amount_block = await CtrGWPayment(current_user).ctr_gw_payment_amount_block(
        account_number=account_number,
        account_amount_block=account_amount_block
    )
    # TODO chờ core trả trường hợp thành công
    return ResponseData(**gw_payment_amount_block)
