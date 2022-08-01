from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.controller import (
    CtrGWEbankIbMb
)
from app.api.v1.endpoints.third_parties.gw.ebank_ib_mb.schema import (
    CheckUsernameIBMBExistRequest, CheckUsernameIBMBExistResponse,
    RetrieveIBInfoByCifRequest, RetrieveIBInfoByCifResponse,
    RetrieveMBInfoByCifRequest, RetrieveMBInfoByCifResponse
)
from app.utils.constant.gw import (
    GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT,
    GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_OUT, GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_OUT
)

router = APIRouter()


@router.post(
    path="/check-username-ib-mb-exist/",
    name="[GW] Kiểm tra Tên đăng nhập ebanking có tồn tại trên Ebank không?",
    description="[GW] Kiểm tra Tên đăng nhập ebanking có tồn tại trên Ebank không?",
    responses=swagger_response(
        response_model=ResponseData[CheckUsernameIBMBExistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_check_username_ib_mb_exist(
        request: CheckUsernameIBMBExistRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_check_username_ib_mb_exist = await CtrGWEbankIbMb(
        current_user).ctr_gw_check_username_ib_mb_exist(
        transaction_name=request.transaction_info.transaction_name,
        transaction_value=request.transaction_info.transaction_value
    )

    gw_get_check_username_ib_mb_exist['data'] = gw_get_check_username_ib_mb_exist.get(
        'data').get(GW_FUNC_CHECK_USERNAME_IB_MB_EXIST_OUT).get('data_output')

    return ResponseData[CheckUsernameIBMBExistResponse](**gw_get_check_username_ib_mb_exist)


@router.post(
    path="/retrieve-ib-info-by-cif/",
    name="[GW] Lấy chi tiết thông tin dịch vụ IB của khách hàng",
    description="[GW] Lấy chi tiết thông tin dịch vụ IB của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[RetrieveIBInfoByCifResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_retrieve_ib_info_by_cif(
        request: RetrieveIBInfoByCifRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_retrieve_ib_info_by_cif = await CtrGWEbankIbMb(
        current_user).ctr_gw_retrieve_ib_info_by_cif(
        cif_num=request.cif_info.cif_num
    )

    gw_get_retrieve_ib_info_by_cif['data'] = gw_get_retrieve_ib_info_by_cif.get(
        'data').get(GW_FUNC_RETRIEVE_IB_INFO_BY_CIF_OUT).get('data_output')

    return ResponseData[RetrieveIBInfoByCifResponse](**gw_get_retrieve_ib_info_by_cif)


@router.post(
    path="/retrieve-mb-info-by-cif/",
    name="[GW] Lấy chi tiết thông tin dịch vụ MB của khách hàng",
    description="[GW] Lấy chi tiết thông tin dịch vụ MB của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[RetrieveMBInfoByCifResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_retrieve_mb_info_by_cif(
        request: RetrieveMBInfoByCifRequest = Body(..., ),
        current_user=Depends(get_current_user_from_header())
):
    gw_get_retrieve_mb_info_by_cif = await CtrGWEbankIbMb(
        current_user).ctr_gw_retrieve_mb_info_by_cif(
        cif_num=request.cif_info.cif_num
    )

    gw_get_retrieve_mb_info_by_cif['data'] = gw_get_retrieve_mb_info_by_cif.get(
        'data').get(GW_FUNC_RETRIEVE_MB_INFO_BY_CIF_OUT).get('data_output')

    return ResponseData[RetrieveMBInfoByCifResponse](**gw_get_retrieve_mb_info_by_cif)
