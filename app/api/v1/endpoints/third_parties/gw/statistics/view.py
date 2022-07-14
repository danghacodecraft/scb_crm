from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.statistics.controller import (
    CtrGWStatistic
)
from app.api.v1.endpoints.third_parties.gw.statistics.schema import (
    SelectStatisticBankingByPeriodDataOutput,
    SelectStatisticBankingByPeriodRequest
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
