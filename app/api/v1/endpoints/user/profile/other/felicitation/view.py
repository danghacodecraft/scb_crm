from fastapi import APIRouter
from starlette import status

from app.api.base.schema import PagingResponse
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.other.felicitation.controller import (
    CtrFelicitation
)
from app.api.v1.endpoints.user.profile.other.felicitation.schema import (
    FelicitionResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - A. KHEN THƯỞNG",
    description="[THÔNG TIN KHÁC] - A. KHEN THƯỞNG",
    responses=swagger_response(
        response_model=PagingResponse[FelicitionResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_current_user(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrFelicitation().ctr_felicitation()
    return PagingResponse[FelicitionResponse](**user_info)
