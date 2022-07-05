from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.deposit.controller import CtrConfigDeposit
from app.api.v1.endpoints.config.deposit.schema import (
    AccClassRequest, AccClassResponse
)
from app.api.v1.schemas.utils import DropdownResponse

router = APIRouter()


@router.get(
    path="/rollover-type/",
    name="Chỉ định khi đến hạn",
    description="Chỉ định khi đến hạn",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_business_type(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    rollover_type = await CtrConfigDeposit(current_user).ctr_get_rollover_type()

    return ResponseData[List[DropdownResponse]](**rollover_type)


@router.get(
    path="/interest-type/",
    name="Hình thức lãi",
    description="Hình thức lãi",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_interest_type(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    interest_type = await CtrConfigDeposit(current_user).ctr_get_interest_type()

    return ResponseData[List[DropdownResponse]](**interest_type)


@router.get(
    path="/acc_type/",
    name="Sản phẩm",
    description="Sản phẩm",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_acc_type(
        current_user=Depends(get_current_user_from_header())  # noqa
):
    acc_type = await CtrConfigDeposit(current_user).ctr_get_acc_type()

    return ResponseData(**acc_type)


@router.get(
    path="/acc_class/",
    name="Loại nhóm sản phẩm (gói) tài khoản",
    description="Loại nhóm sản phẩm (gói) tài khoản",
    responses=swagger_response(
        response_model=ResponseData[List[AccClassResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_acc_class(
        acc_class_request: AccClassRequest = Body(...),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    acc_class = await CtrConfigDeposit(current_user).ctr_get_acc_class(
        acc_class_request=acc_class_request
    )
    return ResponseData[List[AccClassResponse]](**acc_class)
