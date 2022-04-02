from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
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
        employee_id: str = Query(..., description="employee_id")
):
    user_info = await CtrWorkProfile().ctr_work_profile(employee_id=employee_id)
    return ResponseData[WorkProfileInfoResponse](**user_info)
