from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.gis.branchgeojson.controller import (
    CtrBranchgeojson
)
from app.api.v1.endpoints.config.gis.branchgeojson.schema import (
    BranchgeojsonResponse
)

router = APIRouter()


@router.get(
    path="/branchgeojson/",
    name="branchgeojson",
    description="Lấy dữ liệu branchgeojson",
    responses=swagger_response(
        response_model=ResponseData[BranchgeojsonResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_branchgeojson(
        current_user=Depends(get_current_user_from_header())
):
    branchgeojson = await CtrBranchgeojson(current_user).ctr_branchgeojson()
    return ResponseData[BranchgeojsonResponse](**branchgeojson)
