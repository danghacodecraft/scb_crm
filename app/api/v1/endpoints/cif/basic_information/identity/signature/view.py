from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.signature.controller import (
    CtrSignature
)
from app.api.v1.endpoints.cif.basic_information.identity.signature.schema import (
    SignaturesRequest, SignaturesSuccessResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="1. GTĐD - D. Chữ ký",
    description="Tạo dữ liệu tab `CHỮ KÝ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_create_signature(
        signatures: SignaturesRequest,  # TODO: Thêm example
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    signature_data_request = await CtrSignature(current_user).ctr_save_signature(cif_id, signatures)
    return ResponseData[SaveSuccessResponse](**signature_data_request)


@router.get(
    path="/",
    name="1. GTĐD - D. Chữ ký",
    description="Lấy dữ liệu tab `CHỮ KÝ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[List[SignaturesSuccessResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_signature(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    signature_data = await CtrSignature(current_user).ctr_get_signature(cif_id)
    return ResponseData[List[SignaturesSuccessResponse]](**signature_data)
