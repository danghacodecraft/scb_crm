from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
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
async def view_it(
        current_user=Depends(get_current_user_from_header())
):
    it = await CtrIt(current_user).ctr_it()
    return ResponseData[List[ITLevelInfoResponse]](**it)
