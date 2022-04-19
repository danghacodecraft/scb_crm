from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.controller import CtrProfile
from app.api.v1.endpoints.user.profile.schema import ProfileResponse

router = APIRouter()


@router.get(
    path="/",
    name="Thông tin chi tiết nhân viên",
    description="Thông tin chi tiết nhân viên",
    responses=swagger_response(
        response_model=ResponseData[ProfileResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_profile(
        current_user=Depends(get_current_user_from_header())
):
    profile_info = await CtrProfile(current_user).ctr_profile()
    return ResponseData[ProfileResponse](**profile_info)
