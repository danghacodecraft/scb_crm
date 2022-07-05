from typing import List

from fastapi import APIRouter, Body, Depends, Header, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWCasaAccountByCIFNumberRequest,
    GWReportStatementHistoryTDAccountInfoResponse
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.controller import (
    CtrGWDepositAccount
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.example import (
    DEPOSIT_ACCOUNT_BY_CIF_NUMBER_SUCCESS_EXAMPLE, DEPOSIT_ACCOUNT_NUMBER,
    DEPOSIT_ACCOUNT_TD_SUCCESS_EXAMPLE, DEPOSIT_CIF_NUMBER_REQUEST,
    STATEMENT_DEPOSIT_ACCOUNT_TD_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.deposit_account.schema import (
    GWColumnChartDepositAccountRequest, GWColumnChartDepositAccountResponse,
    GWDepositAccountByCIFNumberResponse, GWDepositAccountTDResponse,
    GWDepositOpenAccountTD, GWReportStatementHistoryTDAccountInfoRequest
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Danh sách Tài khoản tiết kiệm theo số CIF",
    description="[GW] Tìm kiếm danh sách Tài khoản tiết kiệm theo số CIF",
    responses=swagger_response(
        response_model=ResponseData[GWDepositAccountByCIFNumberResponse],
        success_examples=DEPOSIT_ACCOUNT_BY_CIF_NUMBER_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_deposit_account_by_cif_number(
        request: GWCasaAccountByCIFNumberRequest = Body(..., example=DEPOSIT_CIF_NUMBER_REQUEST),
        current_user=Depends(get_current_user_from_header())
):
    gw_deposit_account = await CtrGWDepositAccount(current_user).ctr_gw_get_deposit_account_by_cif_number(
        cif_number=request.cif_number
    )
    return ResponseData[GWDepositAccountByCIFNumberResponse](**gw_deposit_account)


@router.post(
    path="/statement/",
    name="[GW] Lịch sử giao dịch tài khoản tiết kiệm",
    description="[GW] Sao kê giao dịch theo số tài khoản tiết kiệm ( lịch sử giao dịch tài khoản tiết kiệm)",
    responses=swagger_response(
        response_model=ResponseData[List[GWReportStatementHistoryTDAccountInfoResponse]],
        success_examples=STATEMENT_DEPOSIT_ACCOUNT_TD_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_statement_deposit_account_td_info(
        request: GWReportStatementHistoryTDAccountInfoRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_statement_account_td_info = await CtrGWDepositAccount(current_user).ctr_gw_get_statement_deposit_account_td(
        request=request
    )
    return ResponseData[List[GWReportStatementHistoryTDAccountInfoResponse]](**gw_statement_account_td_info)


@router.post(
    path="/column-chart/",
    name="[Gw] Biểu Đồ Cột",
    description="Thống kê biến động doanh số tiền gửi bình quân trong 6 tháng (biểu đồ cột màn hình tiền gửi)",
    responses=swagger_response(
        response_model=ResponseData[List[GWColumnChartDepositAccountResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_column_chart_deposit_account_info(
        request: GWColumnChartDepositAccountRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_column_chart_deposit_account_info = await CtrGWDepositAccount(
        current_user
    ).ctr_gw_get_column_chart_deposit_account_info(
        request=request
    )
    return ResponseData[List[GWColumnChartDepositAccountResponse]](**gw_column_chart_deposit_account_info)


@router.post(
    path="/openTD/",
    name="[Tài khoản tiết kiệm] Khởi tạo tài khoản tiết kiệm",
    description="Khởi tạo tài khoản tiết kiệm",
    responses=swagger_response(
        response_model=ResponseData[GWDepositOpenAccountTD],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_deposit_open_account_td(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),
        current_user=Depends(get_current_user_from_header())
):
    gw_deposit_open_account_td = await CtrGWDepositAccount(current_user).ctr_gw_deposit_open_account_td(BOOKING_ID=BOOKING_ID)
    return ResponseData(**gw_deposit_open_account_td)


@router.post(
    path="/{account_number}/",
    name="[Thông tin tài khoản] Chi tiết tài khoản tiết kiệm",
    description="Lấy chi tiết thông tin TK tiền gửi theo Số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWDepositAccountTDResponse],
        success_examples=DEPOSIT_ACCOUNT_TD_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_deposit_account_td(
        account_number: str = Path(..., description="Số tài khoản", example=DEPOSIT_ACCOUNT_NUMBER),
        current_user=Depends(get_current_user_from_header())
):
    gw_deposit_account_td = await CtrGWDepositAccount(current_user).ctr_gw_get_deposit_account_td(
        account_number=account_number
    )
    return ResponseData[GWDepositAccountTDResponse](**gw_deposit_account_td)
