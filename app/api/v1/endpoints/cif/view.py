from typing import List

from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.controller import CtrCustomer
from app.api.v1.endpoints.cif.schema import (
    CareerInformationContactInformationResponse, CheckExistCIFRequest,
    CheckExistCIFSuccessResponse, CifCustomerInformationResponse,
    CifInformationResponse, CifProfileHistoryResponse, CloneCifResponse,
    CustomerByCIFNumberRequest, CustomerByCIFNumberResponse
)

router = APIRouter()


@router.get(
    path="/{cif_id}/",
    name="CIF",
    description="Lấy dữ liệu tab `THÔNG TIN CIF` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CifInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_cif_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())  # noqa
):
    cif_info = await CtrCustomer().ctr_cif_info(cif_id)
    return ResponseData[CifInformationResponse](**cif_info)


@router.get(
    path="/{cif_id}/log/",
    name="Profile history",
    description="Lấy dữ liệu tab `LỊCH SỬ HỒ SƠ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[CifProfileHistoryResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_profile_history(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    profile_history = await CtrCustomer(current_user).ctr_profile_history(cif_id)
    return ResponseData[List[CifProfileHistoryResponse]](**profile_history)


@router.get(
    path="/{cif_id}/customer/",
    name="Customer Information",
    description="Lấy dữ liệu `THÔNG TIN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CifCustomerInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_customer(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    customer_information_data = await CtrCustomer(current_user).ctr_customer_information(cif_id, booking_id=BOOKING_ID)
    return ResponseData[CifCustomerInformationResponse](**customer_information_data)


@router.get(
    path="/{cif_id_or_number}/working-info/",
    name="Customer working information",
    description="Lấy dữ liệu `THÔNG TIN LÀM VIỆC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CareerInformationContactInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_customer_working_info_by_cif_number(
        cif_id_or_number: str = Path(..., description='Id CIF ảo hoặc CIF number'),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrCustomer(current_user).ctr_retrieve_customer_working_info_by_cif_number(
        cif_id_or_number=cif_id_or_number,
    )

    return ResponseData[CareerInformationContactInformationResponse](**customer_information)


@router.post(
    path="/check-exist/",
    name="Kiểm tra tồn tại",
    description="Kiểm tra số CIF có tồn tại hay không",
    responses=swagger_response(
        response_model=ResponseData[CheckExistCIFSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_check_exist_cif(
        request_body: CheckExistCIFRequest,
        current_user=Depends(get_current_user_from_header())
):
    check_exist_data = await CtrCustomer(current_user).ctr_check_exist_cif(cif_number=request_body.cif_number)
    return ResponseData[CheckExistCIFSuccessResponse](**check_exist_data)


@router.post(
    path="/",
    name="Lấy dữ liệu thông tin của khách hàng thông qua số CIF",
    description="Lấy dữ liệu thông tin của khách hàng thông qua số CIF",
    responses=swagger_response(
        response_model=ResponseData[CustomerByCIFNumberResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_customer_information_by_cif_number(
        request: CustomerByCIFNumberRequest = Body(..., description="Thông tin khách hàng qua số CIF"),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrCustomer(current_user).ctr_retrieve_customer_information_by_cif_number(
        request=request
    )
    return ResponseData[CustomerByCIFNumberResponse](**customer_information)


@router.post(
    path="/{cif_id}/clone/",
    name="Clone CIF",
    description="Clone CIF",
    responses=swagger_response(
        response_model=ResponseData[CloneCifResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_clone_cif(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    response = await CtrCustomer().ctr_clone_cif(cif_id)
    return ResponseData[CloneCifResponse](**response)
