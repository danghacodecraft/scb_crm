from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import CreatedUpdatedBaseModel, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.other_information.controller import CtrOtherInfo
from app.api.v1.endpoints.cif.other_information.schema import (
    OtherInformationResponse, OtherInformationUpdateRequest
)

router = APIRouter()


@router.get(
    path="/",
    name="Detail",
    description="Lấy dữ liệu tab `II. THÔNG TIN KHÁC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[OtherInformationResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_other_info(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    other_info = await CtrOtherInfo(current_user).ctr_other_info(cif_id)
    return ResponseData[OtherInformationResponse](**other_info)


@router.post(
    path="/",
    name="Update",
    description="Cập nhật dữ liệu tab `II. THÔNG TIN KHÁC` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[CreatedUpdatedBaseModel],
        success_status_code=status.HTTP_200_OK,
    ),
)
async def view_update_other_info(
        update_other_info_req: OtherInformationUpdateRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    update_other_info = await CtrOtherInfo(current_user).ctr_update_other_info(cif_id, update_other_info_req)
    return ResponseData[CreatedUpdatedBaseModel](**update_other_info)
