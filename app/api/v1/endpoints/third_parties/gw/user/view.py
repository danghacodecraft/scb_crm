from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.user.controller import CtrGWUser
from app.api.v1.endpoints.third_parties.gw.user.schema import (
    GWDetailUserInfoResponse
)

router = APIRouter()


@router.post(
    path="/{user_id}/",
    name="[GW] Select User Info By User Id",
    description="Lấy thông tin user trên CoreFCC",
    responses=swagger_response(
        response_model=ResponseData[List[GWDetailUserInfoResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_amount_block(
        user_id: str = Path(..., description="User ID"),
        current_user=Depends(get_current_user_from_header())
):
    gw_detail_user = await CtrGWUser(current_user).ctr_gw_detail_user(user_id=user_id)

    return ResponseData[List[GWDetailUserInfoResponse]](**gw_detail_user)
