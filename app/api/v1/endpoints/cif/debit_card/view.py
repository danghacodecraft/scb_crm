from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.debit_card.controller import CtrDebitCard
from app.api.v1.endpoints.cif.debit_card.schema import (
    DebitCardRequest, DebitCardResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="Detail Debit Card",
    description="Lấy dữ liệu tab `V. THẺ GHI NỢ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[DebitCardResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_debit_card(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    debit_card = await CtrDebitCard(current_user).ctr_debit_card(cif_id)
    return ResponseData[DebitCardResponse](**debit_card)


@router.post(
    path="/",
    name="Chi tiết thẻ ghi nợ",
    description="Lưu dữ liệu tab `V. THẺ GHI NỢ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[DebitCardRequest],
        success_status_code=status.HTTP_200_OK,
    ),
)
async def view_add_debit_card(
        debt_card_req: DebitCardRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    add_debt_card = await CtrDebitCard(current_user).ctr_add_debit_card(cif_id, debt_card_req)
    return ResponseData[SaveSuccessResponse](**add_debt_card)
