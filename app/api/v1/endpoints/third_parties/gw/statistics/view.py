from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.statistics.controller import (
    CtrGWStatistic
)
from app.api.v1.endpoints.third_parties.gw.statistics.schema import (
    SelectDataForChardDashBoardRequest, SelectDataForChardDashBoardResponse,
    SelectStatisticBankingByPeriodDataOutput,
    SelectStatisticBankingByPeriodRequest, SelectSummaryCardsByDateRequest,
    SelectSummaryCardsByDateResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Lấy thông tin tổng hợp nghiệp vụ ngân hàng từ ngày đến ngày",
    description="[GW] Lấy thông tin tổng hợp nghiệp vụ ngân hàng từ ngày đến ngày",
    responses=swagger_response(
        response_model=ResponseData[SelectStatisticBankingByPeriodDataOutput],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_statistic_banking_by_period(
        request: SelectStatisticBankingByPeriodRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_statistic_banking_by_period = await CtrGWStatistic(current_user).ctr_gw_select_statistic_banking_by_period(
        request=request
    )
    return ResponseData[SelectStatisticBankingByPeriodDataOutput](**gw_select_statistic_banking_by_period)


@router.post(
    path="/select-summary-card-by-date/",
    name="[GW] Lấy thông tin phát hành và doanh số Thẻ ghi nợ + Thẻ tín dụng quốc tế",
    description="[GW] Lấy thông tin phát hành và doanh số Thẻ ghi nợ + Thẻ tín dụng quốc tế",
    responses=swagger_response(
        response_model=ResponseData[SelectSummaryCardsByDateResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_summary_card_by_date(
        request: SelectSummaryCardsByDateRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_summary_card_by_date = await CtrGWStatistic(current_user).ctr_gw_select_summary_card_by_date(
        request=request
    )
    return ResponseData(**gw_select_summary_card_by_date)


@router.post(
    path="/select-data-for-chard-dashboard/",
    name="[GW] Select Data For Chart Dash Board",
    description="Bulleted list:"
    + "\n" + "* Lấy số lượng khách hàng doanh nghiệp mở mới"
    + "\n" + "* Lấy số lượng khách hàng cá nhân mở mới"
    + "\n" + "* Lấy số lượng khoản vay cầm cố"
    + "\n" + "* Lấy số lượng mở Thẻ (ghi nợ + tín dụng)"
    + "\n" + "* Lấy số lượng tất toán tài khoản tiết kiệm"
    + "\n" + "* Lấy số lượng mở tài khoản tiết kiệm"
    + "\n" + "* Lấy số lượng mở cif"
    + "\n" + "* Lấy tổng số bút toán",
    responses=swagger_response(
        response_model=ResponseData[SelectDataForChardDashBoardResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_select_data_for_chard_dashboard(
        request: SelectDataForChardDashBoardRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_select_data_for_chard_dashboard = await CtrGWStatistic(current_user).ctr_gw_select_data_for_chard_dashboard(
        request=request
    )
    return ResponseData[SelectDataForChardDashBoardResponse](**gw_select_data_for_chard_dashboard)
