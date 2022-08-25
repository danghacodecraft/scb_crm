from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.controller import CtrUser
from app.api.v1.endpoints.user.schema import (
    EXAMPLE_RES_FAIL_LOGIN, EXAMPLE_RES_SUCCESS_DETAIL_USER, AuthResponse,
    RefreshTokenResponse, UserBannerResponse
)

router = APIRouter()
security = HTTPBasic()


@router.get(
    path="/banner/",
    name="List Application Banner",
    description="Lấy thông tin danh sách Application Banner",
    responses=swagger_response(
        response_model=ResponseData[Optional[List[UserBannerResponse]]],
        success_status_code=status.HTTP_200_OK,
    )
)
async def view_retrieve_banner(
        is_tablet: bool = Query(False, description='Tablet thì gửi lên True để lấy link ảnh là link ip')
):
    list_banner_info = await CtrUser(is_init_oracle_session=False).ctr_get_banner_info(is_tablet=is_tablet)
    return ResponseData[Optional[List[UserBannerResponse]]](**list_banner_info)


@router.post(
    path="/login/",
    name="Login",
    description="**Đăng nhập:**" + " \n" + "* TUONGHD/Admin@1234",
    responses=swagger_response(
        response_model=ResponseData[AuthResponse],
        success_status_code=status.HTTP_200_OK,
        fail_examples=EXAMPLE_RES_FAIL_LOGIN,
        success_examples=EXAMPLE_RES_SUCCESS_DETAIL_USER
    ),
)
async def view_login(credentials: HTTPBasicCredentials = Depends(security)) -> ResponseData[AuthResponse]:
    data = await CtrUser(is_init_oracle_session=False).ctr_login(credentials)
    return ResponseData[AuthResponse](**data)


@router.post(
    path="/token/",
    name="Refresh Token",
    description="**Refresh Token**",
    responses=swagger_response(
        response_model=ResponseData[RefreshTokenResponse],
        success_status_code=status.HTTP_200_OK,
        # fail_examples=EXAMPLE_RES_FAIL_LOGIN,
        # success_examples=EXAMPLE_RES_SUCCESS_DETAIL_USER
    ),
)
async def view_refresh_token(
        current_user=Depends(get_current_user_from_header(refresh_token=True))
) -> RefreshTokenResponse:
    return ResponseData[RefreshTokenResponse](data=current_user)
