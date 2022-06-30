from typing import Union

from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.top_up.controller import CtrPayInCash
from app.api.v1.endpoints.casa.top_up.schema import (
    PayInCashResponse, PayInCashSCBToAccountRequest, PayInCashSCBByIdentity, PayInCashThirdPartyToAccount,
    PayInCashThirdPartyByIdentity, PayInCashThirdParty247ToAccount, PayInCashThirdParty247ToCard
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
async def view_save_top_up_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: Union[
            PayInCashSCBToAccountRequest,
            PayInCashSCBByIdentity,
            PayInCashThirdPartyToAccount,
            PayInCashThirdPartyByIdentity,
            PayInCashThirdParty247ToAccount,
            PayInCashThirdParty247ToCard
        ] = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    top_up_info = await CtrPayInCash(current_user).ctr_save_top_up_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData(**top_up_info)


@router.get(
    path="/top-up/",
    name="Nộp tiền",
    description="Nộp tiền",
    responses=swagger_response(
        response_model=ResponseData[PayInCashResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_top_up_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):

    get_top_up_info = await CtrPayInCash(current_user).ctr_get_top_up_info(
        booking_id=BOOKING_ID
    )
    return ResponseData[PayInCashResponse](**get_top_up_info)
