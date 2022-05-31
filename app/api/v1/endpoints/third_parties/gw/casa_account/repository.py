from datetime import date

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWAccountInfoOpenCasaRequest, GWCIFInfoOpenCasaRequest,
    GWStaffInfoCheckerOpenCasaRequest, GWStaffInfoMakerOpenCasaRequest,
    GWUdfInfoOpenCasaRequest
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.utils.constant.gw import (
    GW_TRANSACTION_NAME_COLUMN_CHART, GW_TRANSACTION_NAME_PIE_CHART,
    GW_TRANSACTION_NAME_STATEMENT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW


async def repos_gw_get_casa_account_by_cif_number(
        cif_number: str, current_user: AuthResponse
):
    is_success, casa_accounts = await service_gw.get_casa_account_from_cif(
        casa_cif_number=cif_number, current_user=current_user.user_info
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(casa_accounts)
        )

    return ReposReturn(data=casa_accounts)


async def repos_gw_get_casa_account_info(
        account_number: str,
        current_user: str
):
    is_success, gw_casa_account_info = await service_gw.get_casa_account(
        current_user=current_user,
        account_number=account_number
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_casa_account_info)
        )

    return ReposReturn(data=gw_casa_account_info)


async def repos_gw_get_pie_chart_casa_account_info(
    account_number: str,
    current_user: str,
):
    is_success, gw_report_history_account_info = await service_gw.get_report_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_PIE_CHART
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_report_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_history_account_info)
        )

    return ReposReturn(data=gw_report_history_account_info)


async def repos_gw_get_column_chart_casa_account_info(
    account_number: str,
    current_user: str,
    from_date: date,
    to_date: date
):
    is_success, gw_report_column_chart_casa_account_info = await service_gw.get_report_history_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_COLUMN_CHART,
        from_date=from_date,
        to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_report_column_chart_casa_account_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_column_chart_casa_account_info)
        )

    return ReposReturn(data=gw_report_column_chart_casa_account_info)


async def repos_gw_get_statements_casa_account_info(
    account_number: str,
    current_user: str,
    from_date: date,
    to_date: date
):
    is_success, gw_report_history_account_info = await service_gw.get_report_statement_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_STATEMENT,
        from_date=from_date,
        to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_report_statement_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_history_account_info)
        )

    return ReposReturn(data=gw_report_history_account_info)


async def repos_gw_get_open_casa_account(
    cif_info: GWCIFInfoOpenCasaRequest,
    account_info: GWAccountInfoOpenCasaRequest,
    staff_info_checker: GWStaffInfoCheckerOpenCasaRequest,
    staff_info_maker: GWStaffInfoMakerOpenCasaRequest,
    udf_info: GWUdfInfoOpenCasaRequest
):
    is_success, gw_open_casa_account_info = await service_gw.get_open_casa_account(
        cif_info=cif_info, account_info=account_info, staff_info_checker=staff_info_checker,
        staff_info_maker=staff_info_maker, udf_info=udf_info
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_open_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_open_casa_account_info)
        )

    return ReposReturn(data=gw_open_casa_account_info)
