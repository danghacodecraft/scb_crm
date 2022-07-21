from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.ebank.controller import (
    CtrGWRetrieveEbank
)
from app.api.v1.endpoints.third_parties.gw.ebank.example import (
    OPEN_INTERNET_BANKING_REQUEST,
    RETRIEVE_EBANK_BY_CIF_NUMBER_SUCCESS_EXAMPLE,
    RETRIEVE_EBANK_CIF_NUMBER_REQUEST
)
from app.api.v1.endpoints.third_parties.gw.ebank.schema import (
    GWOpenIbRequest, GWRetrieveEbankByCIFNumberRequest,
    GWRetrieveEbankByCIFNumberResponse
)

router = APIRouter()


@router.post(
    path="/retrieve-ebank/",
    name="[GW] Lấy thông tin trạng thái dịch vụ Ebank của khách hàng (SMS, IB/MB) theo Cif",
    description="[GW] Lấy thông tin trạng thái dịch vụ Ebank của khách hàng (SMS, IB/MB) theo Cif",
    responses=swagger_response(
        response_model=ResponseData[List[GWRetrieveEbankByCIFNumberResponse]],
        success_examples=RETRIEVE_EBANK_BY_CIF_NUMBER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_retrieve_ebank_by_cif(
        request: GWRetrieveEbankByCIFNumberRequest = Body(..., example=RETRIEVE_EBANK_CIF_NUMBER_REQUEST),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_retrieve_ebank_by_cif = await CtrGWRetrieveEbank(current_user).ctr_gw_get_retrieve_ebank_by_cif_number(
        cif_num=request.cif_info.cif_num
    )
    return ResponseData[List[GWRetrieveEbankByCIFNumberResponse]](**gw_get_retrieve_ebank_by_cif)


@router.post(
    path="/open-ib/",
    name="[GW] Khởi tạo tài khoản Internet Banking",
    description="[GW] Khởi tạo tài khoản Internet Banking",
    responses=swagger_response(
        response_model=ResponseData,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_open_ib(
        request: GWOpenIbRequest = Body(..., example=OPEN_INTERNET_BANKING_REQUEST),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_retrieve_ebank_by_cif = await CtrGWRetrieveEbank(current_user).ctr_gw_open_ib(
        request=request
    )
    return ResponseData(**gw_get_retrieve_ebank_by_cif)
