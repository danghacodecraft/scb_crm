from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.personal.controller import (
    CtrPersonal
)
from app.api.v1.endpoints.cif.basic_information.personal.schema import (
    PersonalRequest, PersonalResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="2. Thông tin cá nhân",
    description="Tạo dữ liệu tab `THÔNG TIN CÁ NHÂN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_create_personal(
        personal_request: PersonalRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    personal_data_request = await CtrPersonal(current_user).ctr_save_personal(cif_id, personal_request)
    return ResponseData[SaveSuccessResponse](**personal_data_request)


@router.get(
    path="/",
    name="2. Thông tin cá nhân",
    description="Lấy dữ liệu tab `THÔNG TIN CÁ NHÂN` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[PersonalResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_personal(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    personal_data = await CtrPersonal(current_user).ctr_personal(cif_id)
    return ResponseData[PersonalResponse](**personal_data)
