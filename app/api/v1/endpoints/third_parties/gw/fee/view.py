from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.fee.controller import CtrGWFeeInfo
from app.api.v1.endpoints.third_parties.gw.fee.schema import (
    GWFeeInfoRequest, GWFeeInfoResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Lấy thông tin thuế phí",
    description="Lấy thông tin thuế phí theo mã sản phẩm",
    responses=swagger_response(
        response_model=ResponseData[GWFeeInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_employee_info_from_code(
        current_user=Depends(get_current_user_from_header()),
        request: GWFeeInfoRequest = Body(..., description="Thông tin tiền phí truyền vào")

):
    fee_info = await CtrGWFeeInfo(current_user).ctr_gw_select_fee_from_product_name(
        product_name=request.product_name, trans_amount=request.trans_amount, account_num=request.account_num
    )
    return ResponseData[GWFeeInfoResponse](**fee_info)
