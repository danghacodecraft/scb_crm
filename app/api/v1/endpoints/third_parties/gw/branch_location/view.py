from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.branch_location.controller import (
    CtrGWBranchLocation
)
from app.api.v1.endpoints.third_parties.gw.branch_location.schema import (
    SelectBranchByBranchIdRequest, SelectBranchByRegionIdRequest,
    SelectBranchByRegionIdResponse
)

router = APIRouter()


@router.post(
    path="/by-region-id/",
    name="[GW] Lấy danh sách các đơn vị kinh doanh theo mã vùng",
    description="[GW] Lấy danh sách các đơn vị kinh doanh theo mã vùng",
    responses=swagger_response(
        response_model=ResponseData[SelectBranchByRegionIdResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_branch_by_region_id(
        request: SelectBranchByRegionIdRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_branch_by_region_id = await CtrGWBranchLocation(current_user).ctr_gw_select_branch_by_region_id(
        region_id=request.region_id
    )
    return ResponseData[SelectBranchByRegionIdResponse](**gw_select_branch_by_region_id)


@router.post(
    path="/by-branch-id/",
    name="[GW] Lấy chi tiết các đơn vị kinh doanh theo mã đơn vị",
    description="[GW] Lấy chi tiết các đơn vị kinh doanh theo mã đơn vị",
    responses=swagger_response(
        response_model=ResponseData[SelectBranchByRegionIdResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_branch_by_branch_id(
        request: SelectBranchByBranchIdRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_branch_by_branch_id = await CtrGWBranchLocation(current_user).ctr_gw_select_branch_by_branch_id(
        branch_id=request.branch_id
    )
    return ResponseData[SelectBranchByRegionIdResponse](**gw_select_branch_by_branch_id)
