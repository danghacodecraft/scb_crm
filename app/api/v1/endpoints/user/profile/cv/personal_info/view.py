from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.cv.personal_info.controller import (
    CtrPersonalInfo
)
from app.api.v1.endpoints.user.profile.cv.personal_info.schema import (
    PersonalInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[SƠ YẾU LÍ LỊCH] - A. THÔNG TIN CÁ NHÂN",
    description="[SƠ YẾU LÍ LỊCH] - A. THÔNG TIN CÁ NHÂN",
    responses=swagger_response(
        response_model=ResponseData[PersonalInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_personal_info(
        current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrPersonalInfo(current_user).ctr_personal_info()
    return ResponseData[PersonalInfoResponse](**user_info)
