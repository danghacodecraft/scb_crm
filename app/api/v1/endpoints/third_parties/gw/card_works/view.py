import json

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.card_works.controller import (
    CtrGWCardWorks
)
from app.api.v1.endpoints.third_parties.gw.card_works.schema import (
    OpenCardsRequest, SelectCardInfoRequest, SelectCardInfoResponse
)

router = APIRouter()


@router.post(
    path="/open-cards/",
    name="[GW] Đăng ký phát hành thẻ",
    description="[GW] Đăng ký phát hành thẻ",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_open_cards(
        request: OpenCardsRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_open_cards = await CtrGWCardWorks(current_user).ctr_gw_open_cards(
        data=json.loads(request.json())
    )
    return ResponseData(**gw_open_cards)


@router.post(
    path="/select-card-info/",
    name="[GW] Lấy thông tin nhóm thẻ, loại thẻ, chi tiết Thẻ",
    description="[GW] Lấy thông tin nhóm thẻ, loại thẻ, chi tiết Thẻ",
    responses=swagger_response(
        response_model=SelectCardInfoResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_card_info(
        request: SelectCardInfoRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_card_info = await CtrGWCardWorks(current_user).ctr_gw_select_card_info(
        card_branched=request.card_branched
    )
    return ResponseData(**gw_select_card_info)
