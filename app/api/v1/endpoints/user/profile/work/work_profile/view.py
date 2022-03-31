from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.work.work_profile.controller import (
    CtrWorkProfile
)
from app.api.v1.endpoints.user.profile.work.work_profile.schema import (
    WorkProfileInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[Thông tin hồ sơ công tác] - A. Thông tin hồ sơ công tác",
    description="[Thông tin hồ sơ công tác] - A. Thông tin hồ sơ công tác",
    responses=swagger_response(
        response_model=ResponseData[WorkProfileInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_work_profile(
        current_user=Depends(get_current_user_from_header()) # noqa
):
    user_info = await CtrWorkProfile().ctr_work_profile()
    return ResponseData[WorkProfileInfoResponse](**user_info)
