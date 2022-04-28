from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.gis.region.controller import CtrRegion
from app.api.v1.endpoints.config.gis.region.schema import RegionResponse

router = APIRouter()


@router.get(
    path="/region/",
    name="region",
    description="Lấy dữ liệu region",
    responses=swagger_response(
        response_model=ResponseData[List[RegionResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_region(
        current_user=Depends(get_current_user_from_header())
):
    region = await CtrRegion(current_user).ctr_region()
    return ResponseData[List[RegionResponse]](**region)
