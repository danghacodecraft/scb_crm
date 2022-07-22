from datetime import date

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.event import service_gw
from app.utils.functions import date_to_string


async def repos_gw_select_statistic_banking_by_period(current_user: UserInfoResponse, from_date: date, to_date: date):
    data_input = {
        "from_date": date_to_string(from_date),
        "to_date": date_to_string(to_date)
    }
    gw_select_statistic_banking_by_period = await service_gw.select_statistic_banking_by_period(
        current_user=current_user,
        data_input=data_input
    )
    return ReposReturn(data=gw_select_statistic_banking_by_period)


async def repos_gw_select_summary_card_by_date(
        current_user: UserInfoResponse,
        from_date: date,
        to_date: date,
        region_id: str,
        branch_code: str
):
    data_input = {
        "from_date": date_to_string(from_date),
        "to_date": date_to_string(to_date),
        "region_id": region_id,
        "branch_code": branch_code
    }
    gw_select_summary_card_by_date = await service_gw.select_summary_card_by_date(
        current_user=current_user,
        data_input=data_input
    )
    return ReposReturn(data=gw_select_summary_card_by_date)


async def repos_gw_select_data_for_chard_dashboard(
        current_user: UserInfoResponse,
        from_date: date,
        to_date: date,
        search_name: str,
        region_id: str,
        branch_code: str
):
    data_input = {
        "from_date": date_to_string(from_date),
        "to_date": date_to_string(to_date),
        "p_search_name": search_name,
        "region_id": region_id,
        "branch_code": branch_code
    }

    gw_select_data_for_chard_dashboard = await service_gw.select_data_for_chard_dashboard(
        current_user=current_user,
        data_input=data_input
    )
    return ReposReturn(data=gw_select_data_for_chard_dashboard)
