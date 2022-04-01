from typing import List

from fastapi import APIRouter
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.level.it.controller import CtrIt
from app.api.v1.endpoints.user.profile.level.it.schema import (
    ITLevelInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN TRÌNH ĐỘ] - C. TRÌNH ĐỘ TIN HỌC",
    description="[THÔNG TIN TRÌNH ĐỘ] - C. TRÌNH ĐỘ TIN HỌC",
    responses=swagger_response(
        response_model=ResponseData[List[ITLevelInfoResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrIt().ctr_it()
    return ResponseData[List[ITLevelInfoResponse]](**user_info)
