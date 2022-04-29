from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.fund_refund.controller import CtrFund
from app.api.v1.endpoints.casa.fund_refund.schema import (
    FundRefundRequest, FundRefundResponse
)

router = APIRouter()


@router.get(
    path="/{cif_id}/fund_refund/",
    name="Fund Refund",
    description="Ứng quỹ / Hoàn quỹ",
    responses=swagger_response(
        response_model=ResponseData[FundRefundResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_fund_refund_info(
    cif_id: str = Path(..., description="Id CIF ảo"),
    current_user=Depends(get_current_user_from_header())
):
    fund_info = await CtrFund(current_user).ctr_get_fund_refund_info(cif_id=cif_id)
    return ResponseData[FundRefundResponse](**fund_info)


@router.post(
    path="/{cif_id}/fund_refund/",
    name="Fund Refund",
    description="Ứng quỹ / Hoàn quỹ",
    responses=swagger_response(
        response_model=ResponseData[FundRefundRequest],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_fund_refund_info(
    cif_id: str = Path(..., description="Id CIF ảo"),
    request: FundRefundRequest = Body(..., description="abc"),
    current_user=Depends(get_current_user_from_header())
):
    fund_refund_info = await CtrFund(current_user).ctr_save_fund_refund_info(
        cif_id=cif_id,
        request=request
    )

    return ResponseData[FundRefundRequest](**fund_refund_info)
