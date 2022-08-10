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
    OpenCardsRequest
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
    gw_sopen_cards = await CtrGWCardWorks(current_user).ctr_gw_open_cards(
        data=json.loads(request.json())
    )
    return ResponseData(**gw_sopen_cards)
