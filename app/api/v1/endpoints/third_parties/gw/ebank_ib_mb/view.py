from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.controller import (
    CtrGWEbankIbMb
)
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.schema import (
    CheckUsernameIBMBExistRequest, CheckUsernameIBMBExistResponse
)
from app.utils.constant.gw import GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT

router = APIRouter()


@router.post(
    path="/check-username-ib-mb-exist/",
    name="[GW] Kiểm tra Tên đăng nhập ebanking có tồn tại trên Ebank không?",
    description="[GW] Kiểm tra Tên đăng nhập ebanking có tồn tại trên Ebank không?",
    responses=swagger_response(
        response_model=ResponseData[CheckUsernameIBMBExistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_check_username_ib_mb_exist(
        request: CheckUsernameIBMBExistRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_check_username_ib_mb_exist = await CtrGWEbankIbMb(
        current_user).ctr_gw_check_username_ib_mb_exist(
        transaction_name=request.transaction_info.transaction_name,
        transaction_value=request.transaction_info.transaction_value
    )

    gw_get_check_username_ib_mb_exist['data'] = gw_get_check_username_ib_mb_exist.get(
        'data').get(GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT).get('data_output')

    return ResponseData[CheckUsernameIBMBExistResponse](**gw_get_check_username_ib_mb_exist)
