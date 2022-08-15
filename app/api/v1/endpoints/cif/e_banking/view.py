from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.e_banking.controller import CtrEBanking
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, EBankingResponse, EBankingSMSCasaRequest
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="E-banking",
    description="Tạo dữ liệu tab `E BANKING` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_save_e_banking_and_sms_casa(
        e_banking_info: EBankingRequest = Body(default=None, description="Dữ liệu để tạo E-banking"),
        ebank_sms_casa_info: EBankingSMSCasaRequest = Body(default=None, description="Dữ liệu để đăng ký SMS cho TKTT"),
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_response = await CtrEBanking(current_user).ctr_save_e_banking_and_sms(cif_id, e_banking_info, ebank_sms_casa_info)
    return ResponseData[SaveSuccessResponse](**e_banking_response)


@router.get(
    path="/",
    name="E-banking",
    description="Lấy dữ liệu tab `E BANKING` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[EBankingResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_e_banking(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).ctr_get_e_banking(cif_id)
    return ResponseData[EBankingResponse](**e_banking_data)
