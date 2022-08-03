from fastapi import APIRouter, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.ekyc.controller import CtrEKYC
from app.api.v1.endpoints.ekyc.schema import (
    CreateEKYCCustomerRequest, CreateUpdateEKYCCustomerResponse,
    UpdateEKYCCustomerRequest
)

router = APIRouter()


@router.post(
    path="/",
    name="Tạo thông tin khách hàng EKYC",
    description="Tạo thông tin khách hàng EKYC",
    responses=swagger_response(
        response_model=ResponseData[CreateUpdateEKYCCustomerResponse],
        success_status_code=status.HTTP_201_CREATED
    ),
    status_code=status.HTTP_201_CREATED
)
async def view_create_ekyc_customer(
        request: CreateEKYCCustomerRequest,
        server_auth: str = Header(..., alias="Server-Auth")
):
    create_ekyc_customer_info = await CtrEKYC().ctr_create_ekyc_customer(request=request, server_auth=server_auth)
    return ResponseData[CreateUpdateEKYCCustomerResponse](**create_ekyc_customer_info)


@router.put(
    path="/",
    name="Cập nhật thông tin khách hàng EKYC",
    description="Cập nhật thông tin khách hàng EKYC",
    responses=swagger_response(
        response_model=ResponseData[CreateUpdateEKYCCustomerResponse],
        success_status_code=status.HTTP_201_CREATED
    ),
    status_code=status.HTTP_201_CREATED
)
async def view_update_ekyc_customer(
        request: UpdateEKYCCustomerRequest,
        server_auth: str = Header(..., alias="Server-Auth")
):
    update_ekyc_customer_info = await CtrEKYC().ctr_update_ekyc_customer(request=request, server_auth=server_auth)
    return ResponseData[CreateUpdateEKYCCustomerResponse](**update_ekyc_customer_info)
