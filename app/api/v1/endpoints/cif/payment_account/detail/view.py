from typing import List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.payment_account.detail.controller import (
    CtrPaymentAccount
)
from app.api.v1.endpoints.cif.payment_account.detail.schema import (
    PaymentAccountResponse, SavePaymentAccountRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="A. Chi tiết tài khoản thanh toán",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[PaymentAccountResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    detail_customer_relationship_info = await CtrPaymentAccount().detail(cif_id)
    print(detail_customer_relationship_info)
    return ResponseData[PaymentAccountResponse](
        **detail_customer_relationship_info
    )


@router.post(
    path="/",
    name="A. Chi tiết tài khoản thanh toán",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[SavePaymentAccountRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save(
        cif_id: str = Path(..., description='Id CIF ảo'),
        payment_account_save_request: SavePaymentAccountRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    ctr_customer_relationship = CtrPaymentAccount(current_user)

    save_customer_relationship_info = await ctr_customer_relationship.save(
        cif_id=cif_id,
        payment_account_save_request=payment_account_save_request
    )

    return ResponseData[SaveSuccessResponse](
        **save_customer_relationship_info
    )
