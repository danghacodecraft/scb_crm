from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.currency.controller import CtrConfigCurrency
from app.api.v1.endpoints.config.currency.schema import CurrencyResponse

router = APIRouter()


@router.get(
    path="/currency/",
    name="Currency",
    description="Lấy dữ liệu loại tiền",
    responses=swagger_response(
        response_model=ResponseData[List[CurrencyResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_currency_info(
        current_user=Depends(get_current_user_from_header())
):
    currency_info = await CtrConfigCurrency(current_user).ctr_currency_info()
    return ResponseData[List[CurrencyResponse]](**currency_info)
