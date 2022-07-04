from typing import Union

from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.casa.transfer.controller import CtrCasaTransfer
from app.api.v1.endpoints.casa.transfer.schema import (
    CasaTransferResponse, CasaTransferSCBByIdentityRequest,
    CasaTransferSCBToAccountRequest, CasaTransferSourceAccountListResponse,
    CasaTransferThirdParty247ToAccountRequest,
    CasaTransferThirdParty247ToCardRequest,
    CasaTransferThirdPartyByIdentityRequest,
    CasaTransferThirdPartyToAccountRequest
)

router = APIRouter()


@router.post(
    path="/transfer/",
    name="Chuyển khoản",
    description="Chuyển khoản",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_save_casa_transfer_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: Union[
            CasaTransferSCBToAccountRequest,
            CasaTransferSCBByIdentityRequest,
            CasaTransferThirdPartyToAccountRequest,
            CasaTransferThirdPartyByIdentityRequest,
            CasaTransferThirdParty247ToAccountRequest,
            CasaTransferThirdParty247ToCardRequest
        ] = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    casa_transfer_info = await CtrCasaTransfer(current_user).ctr_save_casa_transfer_info(
        booking_id=BOOKING_ID,
        request=request
    )
    return ResponseData(**casa_transfer_info)


@router.get(
    path="/{cif_number}/transfer/source-accounts",
    name="Danh sách tài khoản nguồn chuyển khoản",
    description="Danh sách tài khoản nguồn chuyển khoản",
    responses=swagger_response(
        response_model=ResponseData[CasaTransferSourceAccountListResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_casa_transfer_source_accounts(
        cif_number: str = Path(..., description="Số CIF"),
        current_user=Depends(get_current_user_from_header())
):

    get_casa_transfer_info = await CtrCasaTransfer(current_user).ctr_source_account_info(
        cif_number=cif_number
    )
    return ResponseData[CasaTransferSourceAccountListResponse](**get_casa_transfer_info)


@router.get(
    path="/transfer/",
    name="Chuyển khoản",
    description="Chuyển khoản",
    responses=swagger_response(
        response_model=ResponseData[CasaTransferResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_get_casa_transfer_info(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):

    get_casa_transfer_info = await CtrCasaTransfer(current_user).ctr_get_casa_transfer_info(
        booking_id=BOOKING_ID
    )
    return ResponseData[CasaTransferResponse](**get_casa_transfer_info)
