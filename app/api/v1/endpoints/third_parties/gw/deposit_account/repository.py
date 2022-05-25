from datetime import date
from typing import Optional

from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.utils.constant.gw import (
    GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF,
    GW_TRANSACTION_NAME_COLUMN_CHART_TD, GW_TRANSACTION_NAME_STATEMENT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_deposit_account_by_cif_number(
        cif_number: str, current_user
):
    current_user = current_user.user_info
    is_success, deposit_account = await service_gw.get_deposit_account_from_cif(
        account_cif_number=cif_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_deposit_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(deposit_account)
        )

    return ReposReturn(data=deposit_account)


async def repos_gw_get_deposit_account_td(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, deposit_account_td = await service_gw.get_deposit_account_td(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_get_deposit_account_td",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(deposit_account_td)
        )

    return ReposReturn(data=deposit_account_td)


async def ctr_gw_get_statement_deposit_account_td(
    account_number: str,
    current_user: str,
    from_date: date,
    to_date: date
):
    is_success, gw_report_history_td_account_info = await service_gw.get_report_statement_td_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_STATEMENT,
        from_date=from_date,
        to_date=to_date
    )

    return ReposReturn(data=gw_report_history_td_account_info)


async def repos_gw_get_column_chart_deposit_account_info(
    account_number: str, current_user, from_date: Optional[date], to_date: Optional[date]
):
    current_user = current_user.user_info
    is_success, gw_get_column_chart_deposit_account_info = await service_gw.select_report_td_from_cif_data_input(
        account_number=account_number,
        current_user=current_user,
        endpoint=GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF,
        transaction_name=GW_TRANSACTION_NAME_COLUMN_CHART_TD,
        from_date=from_date,
        to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_get_column_chart_deposit_account_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_get_column_chart_deposit_account_info)
        )

    return ReposReturn(data=gw_get_column_chart_deposit_account_info)
