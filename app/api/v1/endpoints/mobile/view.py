from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.mobile.controller import CtrIdentityMobile
from app.api.v1.endpoints.mobile.schema import (
    CustomerMobileRequest, IdentityMobileRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/cif/identity/",
    name="Thu thập GTDD",
    description="Thu thập GTDD",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def save_identity_mobile(
        request: IdentityMobileRequest = Depends(IdentityMobileRequest.upload_identity_mobile),
        current_user=Depends(get_current_user_from_header())
):
    response_data = await CtrIdentityMobile(current_user).save_identity_mobile(
        request=request
    )
    return ResponseData(**response_data)


@router.get(
    path="/cif/identity/",
    name="Danh sách GTDD",
    description="Danh sách GTDD",
    responses=swagger_response(
        response_model=ResponseData[CustomerMobileRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def search_identity_mobile(
        search_box: str = Query(None, description='`search box`, nhập không dấu'),
        pagination_params: PaginationParams = Depends(),
        current_user=Depends(get_current_user_from_header())
):
    response_data = await CtrIdentityMobile(current_user, pagination_params).search_identity_mobile(
        search_box=search_box,
    )
    return PagingResponse[CustomerMobileRequest](**response_data)
