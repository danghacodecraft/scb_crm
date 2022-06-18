from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.account.controller import CtrConfigAccount
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/account-type/",
    name="Account Type",
    description="Lấy dữ liệu gói tài khoản",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_account_type_info(
        current_user=Depends(get_current_user_from_header())
):
    account_type_info = await CtrConfigAccount(current_user).ctr_account_type_info()
    return ResponseData[List[DropdownResponse]](**account_type_info)


@router.get(
    path="/account-class/",
    name="Account Class",
    description="Lấy dữ liệu loại hình tài khoản",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_account_class_info(
        customer_category_id=Query(None, description="Loại khách hàng"),
        current_user=Depends(get_current_user_from_header())
):
    account_class_info = await CtrConfigAccount(current_user).ctr_account_class_info(
        customer_category_id=customer_category_id
    )
    return ResponseData[List[DropdownResponse]](**account_class_info)
