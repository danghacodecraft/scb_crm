from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.customer.schema import (
    GWOpenCIFResponse
)
from app.api.v1.endpoints.third_parties.gw.payment.controller import (
    CtrGWPayment
)

router = APIRouter()


@router.post(
    path="/{account_number}/amount-block/",
    name="[GW] Amount Block",
    description="Phong tỏa tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWOpenCIFResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_block(
        current_user=Depends(get_current_user_from_header())
):
    gw_payment_amount_block = await CtrGWPayment(current_user).ctr_gw_payment_amount_block()
    return ResponseData(**gw_payment_amount_block)
