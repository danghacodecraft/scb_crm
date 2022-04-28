from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.gis.area.controller import CtrArea
from app.api.v1.endpoints.config.gis.area.schema import AreaResponse

router = APIRouter()


@router.get(
    path="/area/",
    name="area",
    description="Lấy dữ liệu area",
    responses=swagger_response(
        response_model=ResponseData[List[AreaResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_area(
        current_user=Depends(get_current_user_from_header())
):
    area = await CtrArea(current_user).ctr_area()
    return ResponseData[List[AreaResponse]](**area)
