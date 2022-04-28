from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.gis.branch.controller import CtrBranch
from app.api.v1.endpoints.config.gis.branch.schema import BranchResponse

router = APIRouter()


@router.get(
    path="/branch/",
    name="branch",
    description="Lấy dữ liệu branch",
    responses=swagger_response(
        response_model=ResponseData[List[BranchResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_branch(
        current_user=Depends(get_current_user_from_header())
):
    branch = await CtrBranch(current_user).ctr_branch()
    return ResponseData[List[BranchResponse]](**branch)
