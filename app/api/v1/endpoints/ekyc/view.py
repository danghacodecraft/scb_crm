from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.ekyc.controller import CtrEKYC
from app.api.v1.endpoints.ekyc.schema import CreateEKYCCustomerRequest

router = APIRouter()


@router.post(
    path="/",
    name="Tạo thông tin khách hàng EKYC",
    description="Tạo thông tin khách hàng EKYC",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_201_CREATED
    ),
    status_code=status.HTTP_201_CREATED
)
async def view_create_ekyc_customer(
        request: CreateEKYCCustomerRequest,
        current_user=Depends(get_current_user_from_header())
):
    create_ekyc_customer_info = await CtrEKYC(current_user=current_user).ctr_create_ekyc_customer(request=request)
    return ResponseData(**create_ekyc_customer_info)
