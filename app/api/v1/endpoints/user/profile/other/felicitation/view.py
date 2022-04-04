from typing import List

from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.other.felicitation.controller import (
    CtrFelicitation
)
from app.api.v1.endpoints.user.profile.other.felicitation.schema import (
    FelicitationResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - A. KHEN THƯỞNG",
    description="[THÔNG TIN KHÁC] - A. KHEN THƯỞNG",
    responses=swagger_response(
        response_model=ResponseData[List[FelicitationResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_felicitation(
        # current_user=Depends(get_current_user_from_header())
        employee_id=Query(..., description="employee_id")
):
    felicitation_info = await CtrFelicitation().ctr_felicitation(employee_id=employee_id)
    return ResponseData[List[FelicitationResponse]](**felicitation_info)
