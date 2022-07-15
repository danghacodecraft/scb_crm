from typing import List

from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import BaseSchema, ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.casa_account.example import (
    CASA_ACCOUNT_BY_CIF_NUMBER_SUCCESS_EXAMPLE,
    CASA_ACCOUNT_CHECK_EXIST_FAIL_EXAMPLE,
    CASA_ACCOUNT_CHECK_EXIST_SUCCESS_EXAMPLE,
    CASA_ACCOUNT_INFO_SUCCESS_EXAMPLE, CASA_ACCOUNT_NUMBER,
    CASA_ACCOUNT_NUMBER_REQUEST, CASA_CIF_NUMBER_REQUEST
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWBenNameResponse, GWCasaAccountByCIFNumberRequest,
    GWCasaAccountByCIFNumberResponse, GWCasaAccountCheckExistRequest,
    GWCasaAccountCheckExistResponse, GWCasaAccountResponse,
    GWCloseCasaAccountResponse, GWOpenCasaAccountRequest,
    GWOpenCasaAccountResponse, GWReportColumnChartHistoryAccountInfoRequest,
    GWReportColumnChartHistoryAccountInfoResponse,
    GWReportPieChartHistoryAccountInfoRequest,
    GWReportPieChartHistoryAccountInfoResponse,
    GWReportStatementHistoryAccountInfoRequest,
    GWReportStatementHistoryAccountInfoResponse,
    GWThirdPartyAccountCheckExistResponse, GWTopUpCasaAccountResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Danh sách Tài Khoản thanh toán theo số CIF",
    description="[GW] Tìm kiếm danh sách TK thanh toán theo CIF",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountByCIFNumberResponse],
        success_examples=CASA_ACCOUNT_BY_CIF_NUMBER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_casa_account_by_cif_number(
        request: GWCasaAccountByCIFNumberRequest = Body(
            ..., example=CASA_CIF_NUMBER_REQUEST),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_by_cif_number(
        cif_number=request.cif_number
    )
    return ResponseData[GWCasaAccountByCIFNumberResponse](**customer_information)


@router.post(
    path="/check-exist/",
    name="[GW] Kiểm tra số TK có tồn tại không",
    description="[GW] Kiểm tra số TK thanh toán tự chọn có tồn tại trên CoreFCC",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountCheckExistResponse],
        success_examples=CASA_ACCOUNT_CHECK_EXIST_SUCCESS_EXAMPLE,
        fail_examples=CASA_ACCOUNT_CHECK_EXIST_FAIL_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_casa_account_info(
        request: GWCasaAccountCheckExistRequest = Body(..., example=CASA_ACCOUNT_NUMBER_REQUEST),
        current_user=Depends(get_current_user_from_header())
):
    gw_check_exist_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
        account_number=request.account_number
    )
    return ResponseData[GWCasaAccountCheckExistResponse](**gw_check_exist_casa_account_info)


@router.post(
    path="/pie-chart/",
    name="[GW] Biểu đồ tròn",
    description="[GW] Thống kê số lần và giá trị giao dịch theo số tài khoản thanh toán (biểu đồ tròn màn hình tktt)",
    responses=swagger_response(
        response_model=ResponseData[GWReportPieChartHistoryAccountInfoResponse],
        success_examples=CASA_ACCOUNT_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_pie_chart_casa_account_info(
        request: GWReportPieChartHistoryAccountInfoRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_pie_chart_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_pie_chart_casa_account_info(
        request=request
    )
    return ResponseData[List[GWReportPieChartHistoryAccountInfoResponse]](**gw_pie_chart_casa_account_info)


@router.post(
    path="/column-chart/",
    name="[GW] Biểu đồ cột",
    description="[GW] Thống kê lịch sử giao dịch tiền vào/ tiền ra theo số tài khoản thanh toán(biểu đồ cột mh TKTT)",
    responses=swagger_response(
        response_model=ResponseData[GWReportColumnChartHistoryAccountInfoResponse],
        success_examples=CASA_ACCOUNT_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_column_chart_casa_account_info(
        request: GWReportColumnChartHistoryAccountInfoRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_column_chart_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_column_chart_casa_account_info(
        request=request
    )
    return ResponseData[GWReportColumnChartHistoryAccountInfoResponse](**gw_column_chart_casa_account_info)


@router.post(
    path="/statement/",
    name="[GW] Thông tin giao dịch",
    description="[GW] Sao kê giao dịch theo số tài khoản thanh toán ( lịch sử giao dịch tài khoản thanh toán)",
    responses=swagger_response(
        response_model=ResponseData[GWReportStatementHistoryAccountInfoResponse],
        success_examples=CASA_ACCOUNT_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_statement_casa_account_info(
        request: GWReportStatementHistoryAccountInfoRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_statement_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_statement_casa_account_info(
        request=request
    )
    return ResponseData[List[GWReportStatementHistoryAccountInfoResponse]](**gw_statement_casa_account_info)


@router.post(
    path="/open-casa/",
    name="[GW] Mở tài khoản thanh toán",
    description="[GW] Khởi tạo TK Thanh toán",
    responses=swagger_response(
        response_model=ResponseData[GWOpenCasaAccountResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_open_casa_account(
        request: GWOpenCasaAccountRequest = Body(..., description="Thông tin tài khoản"),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        current_user=Depends(get_current_user_from_header())
):
    gw_open_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_open_casa_account(
        request=request,
        booking_id=BOOKING_ID
    )
    return ResponseData[GWOpenCasaAccountResponse](**gw_open_casa_account_info)


@router.post(
    path="/close-casa/",
    name="[GW] Đóng tài khoản thanh toán",
    description="[GW] Đóng tài khoản thanh toán",
    responses=swagger_response(
        response_model=ResponseData[GWCloseCasaAccountResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_close_casa_account(
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    gw_close_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_close_casa_account(
        booking_id=BOOKING_ID
    )
    return ResponseData[GWCloseCasaAccountResponse](**gw_close_casa_account_info)


@router.post(
    path="/top-up/",
    name="[GW] Nộp tiền",
    description="[GW] Nộp tiền",
    responses=swagger_response(
        response_model=ResponseData[GWTopUpCasaAccountResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_top_up_casa_account(
        current_user=Depends(get_current_user_from_header()),
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch")
):
    top_up_casa_account_info = await CtrGWCasaAccount(current_user=current_user).ctr_gw_top_up_casa_account(
        booking_id=BOOKING_ID
    )
    return ResponseData[GWTopUpCasaAccountResponse](**top_up_casa_account_info)


@router.post(
    path="/{account_number}/",
    name="[GW] Chi tiết tài khoản thanh toán",
    description="[GW] Lấy chi tiết thông tin TK thanh toán theo Số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountResponse],
        success_examples=CASA_ACCOUNT_INFO_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_casa_account_info(
        account_number: str = Path(..., description="Số tài khoản", example=CASA_ACCOUNT_NUMBER),
        current_user=Depends(get_current_user_from_header())
):
    gw_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_info(
        account_number=account_number
    )
    return ResponseData[GWCasaAccountResponse](**gw_casa_account_info)


@router.post(
    path="/ben-name-by-account-number/{account_number}/",
    name="[GW] Lấy tên người thụ hưởng qua số TK",
    description="[GW] Lấy tên người thụ hưởng thông qua số tài khoản ngoài SCB",
    responses=swagger_response(
        response_model=ResponseData[GWBenNameResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_ben_name_by_account_number(
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header())
):
    ben_name = await CtrGWCasaAccount(current_user).ctr_gw_get_retrieve_ben_name_by_account_number(
        account_number=account_number
    )
    return ResponseData[GWBenNameResponse](**ben_name)


@router.post(
    path="/check-exist-third-party-account-number/{account_number}/",
    name="[GW] Kiểm tra số tài khoản ngoài SCB có tồn tại không",
    description="[GW] Kiểm tra số tài khoản ngoài SCB có tồn tại không",
    responses=swagger_response(
        response_model=ResponseData[GWThirdPartyAccountCheckExistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_third_party_account_number(
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header())
):
    is_existed = await CtrGWCasaAccount(current_user).ctr_check_exist_account_number_from_other_bank(
        account_number=account_number
    )

    return ResponseData(**dict(data=dict(
        is_existed=is_existed
    )))


@router.post(
    path="/ben-name-by-card-number/{card_number}/",
    name="[GW] Lấy tên người thụ hưởng qua số thẻ",
    description="[GW] Lấy tên người thụ hưởng thông qua số thẻ ngoài SCB",
    responses=swagger_response(
        response_model=ResponseData[GWBenNameResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_ben_name_by_card_number(
        card_number: str = Path(..., description="Số thẻ"),
        current_user=Depends(get_current_user_from_header())
):
    ben_name = await CtrGWCasaAccount(current_user).ctr_gw_get_retrieve_ben_name_by_card_number(
        card_number=card_number
    )
    return ResponseData[GWBenNameResponse](**ben_name)


@router.post(
    path="/check-exist-third-party-card-number/{card_number}/",
    name="[GW] Kiểm tra số thẻ ngoài SCB có tồn tại không",
    description="[GW] Kiểm tra số thẻ ngoài SCB có tồn tại không",
    responses=swagger_response(
        response_model=ResponseData[GWThirdPartyAccountCheckExistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_third_party_card_number(
        card_number: str = Path(..., description="Số thẻ"),
        current_user=Depends(get_current_user_from_header())
):
    is_existed = await CtrGWCasaAccount(current_user).ctr_check_exist_card_number_from_other_bank(
        card_number=card_number
    )

    return ResponseData(**dict(data=dict(
        is_existed=is_existed
    )))


@router.post(
    path="/change-status-account/{account_number}",
    name="Khóa tài khoản thanh toán (Thay đổi trạng thái nodebit/ nocredit)",
    description="[GW] Khóa tài khoản thanh toán (Thay đổi trạng thái nodebit/ nocredit)",
    responses=swagger_response(
        response_model=ResponseData[BaseSchema],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_change_status_account(
        account_number: str = Path(..., description="Số thẻ"),
        current_user=Depends(get_current_user_from_header())
):
    account_number = await CtrGWCasaAccount(current_user).ctr_gw_change_status_account(
        account_number=account_number
    )

    return ResponseData(**account_number)
