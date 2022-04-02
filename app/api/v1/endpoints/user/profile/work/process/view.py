from typing import List

from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.work.process.controller import (
    CtrProcess
)
from app.api.v1.endpoints.user.profile.work.process.schema import (
    WorkProcessResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[Quá trình công tác] - C. Quá trình công tác",
    description="[Quá trình công tác] - C. Quá trình công tác",
    responses=swagger_response(
        response_model=ResponseData[List[WorkProcessResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_work_process(
        employee_id: str = Query(..., description="employee_id")
):
    user_info = await CtrProcess().ctr_process(employee_id=employee_id)

    return ResponseData[List[WorkProcessResponse]](**user_info)
