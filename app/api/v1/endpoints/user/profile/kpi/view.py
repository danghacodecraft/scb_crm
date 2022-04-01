from typing import List

from fastapi import APIRouter
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.kpi.controller import CtrKpi
from app.api.v1.endpoints.user.profile.kpi.schema import KpiResponse

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KPIS]",
    description="[THÔNG TIN KPIS]",
    responses=swagger_response(
        response_model=ResponseData[List[KpiResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_kpi(
        # current_user=Depends(get_current_user_from_header())
):
    user_info = await CtrKpi().ctr_kpi()
    return ResponseData[List[KpiResponse]](**user_info)
