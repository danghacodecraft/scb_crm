from typing import List

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.guardian.controller import (
    CtrGuardian
)
from app.api.v1.endpoints.cif.basic_information.guardian.schema import (
    DetailGuardianResponse, SaveGuardianRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.get(
    path="/",
    name="5. Thông tin người giám hộ",
    description="Chi tiết",
    responses=swagger_response(
        response_model=ResponseData[DetailGuardianResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_guardian = CtrGuardian(current_user)

    detail_guardian_info = await ctr_guardian.detail(
        cif_id=cif_id
    )

    return ResponseData[DetailGuardianResponse](
        **detail_guardian_info
    )


@router.post(
    path="/",
    name="5. Thông tin người giám hộ",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save(
        cif_id: str = Path(..., description='Id CIF ảo'),
        guardian_save_request: List[SaveGuardianRequest] = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    ctr_guardian = CtrGuardian(current_user)

    save_guardian_info = await ctr_guardian.save(
        cif_id=cif_id,
        guardian_save_request=guardian_save_request
    )

    return ResponseData[SaveSuccessResponse](
        **save_guardian_info
    )
