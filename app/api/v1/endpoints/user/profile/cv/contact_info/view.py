from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.cv.contact_info.controller import (
    CtrContact_Info
)
from app.api.v1.endpoints.user.profile.cv.contact_info.schema import (
    EmployeeContactInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[SƠ YẾU LÍ LỊCH] - B. THÔNG TIN LIÊN HỆ",
    description="[SƠ YẾU LÍ LỊCH] - B. THÔNG TIN LIÊN HỆ",
    responses=swagger_response(
        response_model=ResponseData[EmployeeContactInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_contact_info(
        current_user=Depends(get_current_user_from_header())
):
    contact_info = await CtrContact_Info(current_user).ctr_contact_info()
    return ResponseData[EmployeeContactInfoResponse](**contact_info)
