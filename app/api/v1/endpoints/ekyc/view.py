from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.ekyc.controller import CtrEKYC
from app.api.v1.endpoints.ekyc.schema import (
    CreateEKYCCustomerRequest, CreateEKYCCustomerResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="Tạo/Cập nhật thông tin khách hàng EKYC",
    description="Tạo/Cập nhật thông tin khách hàng EKYC",
    responses=swagger_response(
        response_model=ResponseData[CreateEKYCCustomerResponse],
        success_status_code=status.HTTP_201_CREATED
    ),
    status_code=status.HTTP_201_CREATED
)
async def view_create_ekyc_customer(
        request: CreateEKYCCustomerRequest
):
    create_ekyc_customer_info = await CtrEKYC().ctr_create_ekyc_customer(request=request)
    return ResponseData[CreateEKYCCustomerResponse](**create_ekyc_customer_info)
