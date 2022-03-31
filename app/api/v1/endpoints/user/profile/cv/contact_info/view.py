from fastapi import APIRouter
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.cv.contact_info.controller import (
    CtrContact_Info
)
from app.api.v1.endpoints.user.profile.cv.contact_info.schema import (
    EmployeeInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[SƠ YẾU LÍ LỊCH] - B. THÔNG TIN LIÊN HỆ",
    description="[SƠ YẾU LÍ LỊCH] - B. THÔNG TIN LIÊN HỆ",
    responses=swagger_response(
        response_model=ResponseData[EmployeeInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrContact_Info().ctr_contact_info()
    return ResponseData[EmployeeInfoResponse](**user_info)
