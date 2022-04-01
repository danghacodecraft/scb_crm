from typing import List

from fastapi import APIRouter
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.other.discipline.controller import (
    CtrDiscipline
)
from app.api.v1.endpoints.user.profile.other.discipline.schema import (
    DisciplineResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - B. KỶ LUẬT",
    description="[THÔNG TIN KHÁC] - B. KỶ LUẬT",
    responses=swagger_response(
        response_model=ResponseData[List[DisciplineResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_discipline(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrDiscipline().ctr_discipline()
    return ResponseData[List[DisciplineResponse]](**user_info)
