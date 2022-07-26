import json

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
    GWSelectMobileNumberSMSByAccountCASAResponse,
    RegisterSmsServiceByAccountCasaRequest,
    RegisterSmsServiceByMobileNumberRequest, SelectAccountTDByMobileNumRequest,
    SelectAccountTDByMobileNumResponse
)
from app.utils.constant.gw import (
    GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_OUT,
    GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_OUT,
    GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_OUT,
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
    gw_get_select_mobile_number_sms_by_account_casa['data'] = gw_get_select_mobile_number_sms_by_account_casa.get(
        'data').get(GW_FUNC_SELECT_MOBILE_NUMBER_SMS_BY_ACCOUNT_CASA_OUT).get('data_output')

    return ResponseData[GWSelectMobileNumberSMSByAccountCASAResponse](**gw_get_select_mobile_number_sms_by_account_casa)


@router.post(
    path="/select-account-td-by-mobile-num/",
    name="[GW] Lấy danh sách tài khoản tiết kiệm theo số điện thoại",
    description="[GW] Lấy danh sách tài khoản tiết kiệm theo số điện thoại",
    responses=swagger_response(
        response_model=ResponseData[SelectAccountTDByMobileNumResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_select_account_td_by_mobile_num(
        request: SelectAccountTDByMobileNumRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_select_account_td_by_mobile_num = await CtrGWEbankSms(
        current_user).ctr_gw_select_account_td_by_mobile_num(
        ebank_sms_indentify_num=request.ebank_sms_info.ebank_sms_indentify_num
    )
    gw_get_select_account_td_by_mobile_num['data'] = gw_get_select_account_td_by_mobile_num.get(
        'data').get(GW_FUNC_SELECT_ACCOUNT_TD_BY_MOBILE_NUM_OUT).get('data_output')

    return ResponseData[SelectAccountTDByMobileNumResponse](**gw_get_select_account_td_by_mobile_num)


@router.post(
    path="/register-sms-service-by-account-casa/",
    name="[GW] Đăng ký dịch vụ SMS Banking theo số tài khoản thanh toán",
    description="[GW] Đăng ký dịch vụ SMS Banking theo số tài khoản thanh toán",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_register_sms_service_by_account_casa(
        request: RegisterSmsServiceByAccountCasaRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    request_data = json.loads(request.json())

    gw_get_register_sms_service_by_account_casa = await CtrGWEbankSms(
        current_user).ctr_gw_register_sms_service_by_account_casa(
        account_info=request_data.get('account_info'),
        ebank_sms_info_list=request_data.get('ebank_sms_info_list'),
        staff_info_checker=request_data.get('staff_info_checker'),
        staff_info_maker=request_data.get('staff_info_maker')
    )

    gw_get_register_sms_service_by_account_casa['data'] = gw_get_register_sms_service_by_account_casa.get(
        'data').get(GW_FUNC_REGISTER_SMS_SERVICE_BY_ACCOUNT_CASA_OUT).get('data_output')

    return ResponseData(**gw_get_register_sms_service_by_account_casa)


@router.post(
    path="/register-sms-service-by-mobile-number/",
    name="[GW] Đăng ký dịch vụ SMS Banking cho tài khoản tiết kiệm theo số điện thoại",
    description="[GW] Đăng ký dịch vụ SMS Banking cho tài khoản tiết kiệm theo số điện thoại",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_register_sms_service_by_mobile_number(
        request: RegisterSmsServiceByMobileNumberRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    request_data = json.loads(request.json())

    gw_get_register_sms_service_by_mobile_number = await CtrGWEbankSms(
        current_user).ctr_gw_register_sms_service_by_mobile_number(
        account_info=request_data.get('account_info'),
        customer_info=request_data.get('customer_info'),
        staff_info_checker=request_data.get('staff_info_checker'),
        staff_info_maker=request_data.get('staff_info_maker')
    )

    gw_get_register_sms_service_by_mobile_number['data'] = gw_get_register_sms_service_by_mobile_number.get(
        'data').get(GW_FUNC_REGISTER_SMS_SERVICE_BY_MOBILE_NUMBER_OUT).get('data_output')

    return ResponseData(**gw_get_register_sms_service_by_mobile_number)
