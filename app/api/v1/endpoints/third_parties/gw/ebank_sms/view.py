from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.ebank_sms.controller import (
    CtrGWEbankSms
)
from app.api.v1.endpoints.third_parties.gw.ebank_sms.schema import (
    GWSelectMobileNumberSMSByAccountCASARequest,
    GWSelectMobileNumberSMSByAccountCASAResponse
)
from app.utils.constant.gw import (
    GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_OUT
)

router = APIRouter()


@router.post(
    path="/select-mobile-number-sms-by-account-casa/",
    name="[GW] Lấy danh sách các số điện thoại đăng ký sms theo tài khoản thanh toán",
    description="[GW] Lấy danh sách các số điện thoại đăng ký sms theo tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[GWSelectMobileNumberSMSByAccountCASAResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_select_mobile_number_sms_by_account_casa(
        request: GWSelectMobileNumberSMSByAccountCASARequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_select_mobile_number_sms_by_account_casa = await CtrGWEbankSms(
        current_user).ctr_gw_select_mobile_number_sms_by_account_casa(
        ebank_sms_indentify_num=request.ebank_sms_info.ebank_sms_indentify_num
    )
    gw_get_select_mobile_number_sms_by_account_casa['data'] = gw_get_select_mobile_number_sms_by_account_casa[
        'data'][GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_OUT]['data_output']

    return ResponseData[GWSelectMobileNumberSMSByAccountCASAResponse](**gw_get_select_mobile_number_sms_by_account_casa)
