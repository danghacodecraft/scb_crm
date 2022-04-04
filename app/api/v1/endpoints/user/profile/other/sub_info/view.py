from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
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
        # current_user=Depends(get_current_user_from_header())
        employee_id=Query(..., description="employee_id")
):
    sub_info = await CtrSubInfo().ctr_sub_info(employee_id=employee_id)
    return ResponseData(**sub_info)
    # return ResponseData[SubInfoResponse](**user_info)
