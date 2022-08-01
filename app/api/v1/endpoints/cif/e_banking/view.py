from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import PagingResponse, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.cif.e_banking.controller import CtrEBanking
from app.api.v1.endpoints.cif.e_banking.examples import GET_E_BANKING_SUCCESS
from app.api.v1.endpoints.cif.e_banking.schema import (
    BalancePaymentAccountResponses, BalanceSavingAccountsResponse,
    EBankingRequest, EBankingResponse, EBankingSMSCasaRequest,
    ResetPasswordEBankingResponse, ResetPasswordTellerResponse
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
        e_banking_info: Optional[EBankingRequest] = Body(default=None, description="Dữ liệu để tạo E-banking"),
        ebank_sms_casa_info: Optional[EBankingSMSCasaRequest] = Body(default=None, description="Dữ liệu để đăng ký SMS cho TKTT"),
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
        success_status_code=status.HTTP_200_OK,
        success_examples=GET_E_BANKING_SUCCESS
    ),
)
async def view_retrieve_e_banking(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).ctr_get_e_banking(cif_id)
    return ResponseData[EBankingResponse](**e_banking_data)


@router.get(
    path="/payment-account/",
    name="Danh sách tài khoản thanh toán",
    description="Lấy dữ liệu tab `DANH SÁCH TÀI KHOẢN THANH TOÁN`",
    responses=swagger_response(
        response_model=ResponseData[List[BalancePaymentAccountResponses]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_balance_payment_account(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    balance_payment_account_data = await CtrEBanking(current_user).ctr_balance_payment_account(cif_id)
    return ResponseData[List[BalancePaymentAccountResponses]](**balance_payment_account_data)


@router.get(
    path="/saving-account/",
    name="Danh sách tài khoản tiết kiệm",
    description="Lấy dữ liệu `DANH SÁCH TÀI KHOẢN TIẾT KIỆM`",
    responses=swagger_response(
        response_model=PagingResponse[BalanceSavingAccountsResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_balance_saving_account(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends()
):
    balance_saving_account_data = await CtrEBanking(
        current_user,
        pagination_params=pagination_params
    ).ctr_balance_saving_account(cif_id)
    return PagingResponse[BalanceSavingAccountsResponse](**balance_saving_account_data)


@router.get(
    path="/reset-password/call-center/",
    name="Cấp lại mật khẩu E-Banking call center",
    description="Chi tiết IV. E-Banking - Cấp lại mật khẩu E-Banking call center",
    responses=swagger_response(
        response_model=ResponseData[ResetPasswordEBankingResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_reset_password(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_e_banking = CtrEBanking(current_user)

    e_banking_data = await ctr_e_banking.get_detail_reset_password(cif_id=cif_id)

    return ResponseData[ResetPasswordEBankingResponse](**e_banking_data)


@router.get(
    path="/reset-password/teller/",
    name="Cấp lại mật khẩu E-Banking - Quầy giao dịch",
    description="E-Banking - Cấp lại mật khẩu E-Banking - Quầy giao dịch",
    responses=swagger_response(
        response_model=ResponseData[ResetPasswordTellerResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_reset_password_teller(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).get_detail_reset_password_teller(cif_id=cif_id)

    return ResponseData[ResetPasswordTellerResponse](**e_banking_data)
