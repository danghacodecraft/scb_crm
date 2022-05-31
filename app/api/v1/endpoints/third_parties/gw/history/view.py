from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.history.controller import (
    CtrGWHistory
)
from app.api.v1.endpoints.third_parties.gw.history.example import (
    HISTORY_CHANGE_FIELD_ACCOUNT_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.history.schema import (
    GWHistoryChangeFieldAccount
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] History Change Field Account",
    description="Lịch sử thay đổi trường dữ liệu theo số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[List[GWHistoryChangeFieldAccount]],
        success_examples=HISTORY_CHANGE_FIELD_ACCOUNT_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_history_change_field_account(
        current_user=Depends(get_current_user_from_header())
):
    history_change_field_account = await CtrGWHistory(current_user).ctr_gw_get_history_change_field_account()
    return ResponseData[List[GWHistoryChangeFieldAccount]](**history_change_field_account)
