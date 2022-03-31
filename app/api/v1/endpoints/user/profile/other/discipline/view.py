from fastapi import APIRouter
from starlette import status

from app.api.base.schema import PagingResponse
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.other.discipline.controller import (
    CtrDiscipline
)
from app.api.v1.endpoints.user.profile.other.discipline.schema import (
    DiscriplineResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - B. KỶ LUẬT",
    description="[THÔNG TIN KHÁC] - B. KỶ LUẬT",
    responses=swagger_response(
        response_model=PagingResponse[DiscriplineResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrDiscipline().ctr_discipline()
    return PagingResponse[DiscriplineResponse](**user_info)
