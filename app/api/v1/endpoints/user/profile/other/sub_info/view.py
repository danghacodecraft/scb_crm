from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.other.sub_info.controller import (
    CtrSubInfo
)
from app.api.v1.endpoints.user.profile.other.sub_info.schema import (
    SubInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - D. THÔNG TIN PHỤ",
    description="[THÔNG TIN KHÁC] - D. THÔNG TIN PHỤ",
    responses=swagger_response(
        response_model=ResponseData[SubInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_sub_info(
        current_user=Depends(get_current_user_from_header())

):
    sub_info = await CtrSubInfo(current_user).ctr_sub_info()
    return ResponseData(**sub_info)
