from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.denominations.controller import (
    CtrConfigCurrencyDenomination
)
from app.api.v1.endpoints.config.denominations.schema import (
    CurrencyDenominationResponse
)

router = APIRouter()


@router.get(
    path="/denominations/",
    name="Currency Denominations",
    description="Lấy dữ liệu mệnh giá",
    responses=swagger_response(
        response_model=ResponseData[List[CurrencyDenominationResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_currency_info(
        current_user=Depends(get_current_user_from_header()),
        currency_id: str = Query(..., description="ID loại tiền")
):
    currency_denominations_info = await CtrConfigCurrencyDenomination(current_user).ctr_currency_denominations_info(
        currency_id=currency_id)
    return ResponseData[List[CurrencyDenominationResponse]](**currency_denominations_info)
