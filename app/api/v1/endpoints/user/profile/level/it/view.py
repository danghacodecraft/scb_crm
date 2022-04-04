from typing import List

from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
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
        employee_id: str = Query(..., description="employee_id")
):
    it = await CtrIt().ctr_it(employee_id=employee_id)
    return ResponseData[List[ITLevelInfoResponse]](**it)
