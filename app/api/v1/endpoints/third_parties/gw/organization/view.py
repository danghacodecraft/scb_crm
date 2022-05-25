from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.organization.controller import (
    CtrGWOrganization
)
from app.api.v1.endpoints.third_parties.gw.organization.example import (
    ORGANIZATION_INFO_FROM_CHILD_SUCCESS_EXAMPLE,
    ORGANIZATION_INFO_FROM_PARENT_SUCCESS_EXAMPLE,
    ORGANIZATION_INFO_SUCCESS_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.organization.schema import (
    GWOrgInfoFromChildResponse, GWOrgInfoFromParentResponse, GWOrgInfoResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Lấy tất cả dữ liệu cây tổ chức",
    description="Lấy tất cả dữ liệu cây tổ chức",
    responses=swagger_response(
        response_model=ResponseData[GWOrgInfoResponse],
        success_examples=ORGANIZATION_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_organization_info(
        current_user=Depends(get_current_user_from_header())
):
    organization_info = await CtrGWOrganization(current_user).ctr_gw_get_organization_info()
    return ResponseData[List[GWOrgInfoResponse]](**organization_info)


@router.post(
    path="/from_parent/",
    name="[GW] Lấy dữ liệu cấp cha cây tổ chức",
    description="Lấy dữ liệu cấp cha cây tổ chức",
    responses=swagger_response(
        response_model=ResponseData[GWOrgInfoFromParentResponse],
        success_examples=ORGANIZATION_INFO_FROM_PARENT_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_organization_info_from_parent(
        current_user=Depends(get_current_user_from_header())
):
    organization_info_from_parent = await CtrGWOrganization(current_user).ctr_gw_get_organization_info_from_parent()
    return ResponseData[GWOrgInfoFromParentResponse](**organization_info_from_parent)


@router.post(
    path="/from_child/",
    name="[GW] Lấy dữ liệu cấp con cây tổ chức",
    description="Lấy dữ liệu cấp con cây tổ chức",
    responses=swagger_response(
        response_model=ResponseData[GWOrgInfoFromChildResponse],
        success_examples=ORGANIZATION_INFO_FROM_CHILD_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_organization_info_from_child(
        current_user=Depends(get_current_user_from_header())
):
    organization_info_from_child = await CtrGWOrganization(current_user).ctr_gw_get_organization_info_from_child()
    return ResponseData[List[GWOrgInfoFromChildResponse]](**organization_info_from_child)
