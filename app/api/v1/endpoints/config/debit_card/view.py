from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.debit_card.controller import CtrDebitCard
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/card-issuance-type/",
    name="Card Issuance Type",
    description="Lấy dữ liệu Hình thức phát hành thẻ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_card_issuance_type_info(
        current_user=Depends(get_current_user_from_header()),
):
    card_issuance_type_info = await CtrDebitCard(current_user).ctr_card_issuance_type_info()
    return ResponseData[List](**card_issuance_type_info)


@router.get(
    path="/debit-card-types/",
    name="Debit Card Type",
    description="Lấy dữ liệu Loại thẻ",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_card_type_info(
        current_user=Depends(get_current_user_from_header()),
):
    card_type_info = await CtrDebitCard(current_user).ctr_card_type_info()
    return ResponseData[List](**card_type_info)
