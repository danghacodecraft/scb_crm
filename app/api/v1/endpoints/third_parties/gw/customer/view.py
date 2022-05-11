from typing import Union

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.cif.schema import GWCustomerDetailRequest
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.customer.example import (
    AUTHORIZED_ACCOUNT_NUMBER, COOWNER_ACCOUNT_NUMBER,
    CUSTOMER_AUTHORIZER_SUCCESS_EXAMPLE,
    CUSTOMER_CHECK_EXIST_CIF_ID_FAIL_EXAMPLE,
    CUSTOMER_CHECK_EXIST_CIF_ID_SUCCESS_EXAMPLE, CUSTOMER_CIF_ID,
    CUSTOMER_COOWNER_SUCCESS_EXAMPLE, CUSTOMER_INFO_DETAIL_SUCCESS_EXAMPLE,
    CUSTOMER_INFO_LIST_SUCCESS_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.customer.schema import (
    CustomerInfoListCIFRequest, DebitCardByCIFNumberResponse,
    GuardianOrCustomerRelationshipByCIFNumberResponse,
    GWAuthorizedListResponse, GWCoOwnerListResponse,
    GWCustomerCheckExistRequest, GWCustomerCheckExistResponse,
    GWCustomerInfoDetailResponse, GWCustomerInfoListResponse
)
from app.utils.constant.gw import (
    GW_REQUEST_PARAMETER_DEBIT_CARD,
    GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Lấy thông tin khách hàng",
    description="[GW] Lấy thông tin khách hàng CIF/CMND/CCCD/Số điện thoại/Họ tên KH",
    responses=swagger_response(
        response_model=ResponseData[GWCustomerInfoListResponse],
        success_examples=CUSTOMER_INFO_LIST_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_customer_info_list(
        request: CustomerInfoListCIFRequest = Body(..., example=CUSTOMER_CIF_ID),
        current_user=Depends(get_current_user_from_header())
):
    gw_customer_info_list = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_list(
        cif_number=request.cif_number,
        identity_number=request.identity_number,
        mobile_number=request.mobile_number,
        full_name=request.full_name
    )

    return ResponseData[GWCustomerInfoListResponse](**gw_customer_info_list)


@router.post(
    path="/check-exist/",
    name="[GW] Kiểm tra số CIF có tồn tại không",
    description="[GW] Kiểm tra số CIF tự chọn có tồn tại trên CoreFCC",
    responses=swagger_response(
        response_model=ResponseData[GWCustomerCheckExistResponse],
        success_examples=CUSTOMER_CHECK_EXIST_CIF_ID_SUCCESS_EXAMPLE,
        fail_examples=CUSTOMER_CHECK_EXIST_CIF_ID_FAIL_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_casa_account_info(
        request: GWCustomerCheckExistRequest = Body(..., example=CUSTOMER_CIF_ID),
        current_user=Depends(get_current_user_from_header())
):
    gw_check_exist_casa_account_info = await CtrGWCustomer(current_user).ctr_gw_check_exist_customer_detail_info(
        cif_number=request.cif_number
    )
    return ResponseData[GWCustomerCheckExistResponse](**gw_check_exist_casa_account_info)


@router.post(
    path="/{cif_number}/",
    name="[GW] Lấy chi tiết thông tin khách hàng",
    description="Lấy chi tiết thông tin khách hàng theo CIF",
    responses=swagger_response(
        response_model=Union[
            ResponseData[GWCustomerInfoDetailResponse],
            ResponseData[GuardianOrCustomerRelationshipByCIFNumberResponse],
            ResponseData[DebitCardByCIFNumberResponse]
        ],
        success_examples=CUSTOMER_INFO_DETAIL_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_customer_info_detail(
    cif_number: str = CustomField().CIFNumberPath,
    request: GWCustomerDetailRequest = Body(...),
    current_user=Depends(get_current_user_from_header())
):
    parameter = request.parameter

    gw_customer_info_detail = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
        cif_number=cif_number,
        parameter=parameter
    )

    if parameter == GW_REQUEST_PARAMETER_GUARDIAN_OR_CUSTOMER_RELATIONSHIP:
        return ResponseData[GuardianOrCustomerRelationshipByCIFNumberResponse](**gw_customer_info_detail)

    elif parameter == GW_REQUEST_PARAMETER_DEBIT_CARD:
        return ResponseData[DebitCardByCIFNumberResponse](**gw_customer_info_detail)

    else:
        return ResponseData[GWCustomerInfoDetailResponse](**gw_customer_info_detail)


@router.post(
    path="/{account_number}/co-owner/",
    name="[GW] Lấy dash sách đồng sở hữu theo số tài khoản",
    description="Lấy danh sách đồng sở hữu theo số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWCoOwnerListResponse],
        success_examples=CUSTOMER_COOWNER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_co_owner(
        account_number: str = Path(..., description="Số tài khoản", example=COOWNER_ACCOUNT_NUMBER),
        current_user=Depends(get_current_user_from_header())
):
    gw_customer_co_owner = await CtrGWCustomer(current_user).ctr_gw_get_co_owner(
        account_number=account_number
    )
    return ResponseData[GWCoOwnerListResponse](**gw_customer_co_owner)


@router.post(
    path="/{account_number}/authorized/",
    name="[GW] Lấy danh sách ủy quyền theo tài khoản",
    description="Lấy danh sách ủy quyền theo tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWAuthorizedListResponse],
        success_examples=CUSTOMER_AUTHORIZER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_authorized(
        account_number: str = Path(..., description="Số tài khoản", example=AUTHORIZED_ACCOUNT_NUMBER),
        current_user=Depends(get_current_user_from_header())
):
    gw_customer_authorized = await CtrGWCustomer(current_user).ctr_gw_get_authorized(
        account_number=account_number
    )
    return ResponseData[GWAuthorizedListResponse](**gw_customer_authorized)
