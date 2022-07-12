from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import (
    TdAccount, TdAccountResign
)
from app.third_parties.oracle.models.cif.form.model import (
    BookingAccount, BookingBusinessForm
)
from app.third_parties.oracle.models.master_data.others import TransactionJob
from app.utils.constant.approval import BUSINESS_JOB_CODE_OPEN_TD_ACCOUNT
from app.utils.constant.cif import BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT_PD
from app.utils.constant.gw import (
    GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF,
    GW_TRANSACTION_NAME_COLUMN_CHART_TD, GW_TRANSACTION_NAME_STATEMENT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW
from app.utils.functions import generate_uuid, now, orjson_dumps


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
        cif_number: str, current_user
):
    current_user = current_user.user_info
    is_success, gw_get_column_chart_deposit_account_info = await service_gw.select_report_td_from_cif_data_input(
        cif_number=cif_number,
        current_user=current_user,
        endpoint=GW_ENDPOINT_URL_RETRIEVE_REPORT_TD_FROM_CIF,
        transaction_name=GW_TRANSACTION_NAME_COLUMN_CHART_TD
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="gw_get_column_chart_deposit_account_info",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_get_column_chart_deposit_account_info)
        )

    return ReposReturn(data=gw_get_column_chart_deposit_account_info)


@auto_commit
async def repos_gw_deposit_open_account_td(current_user, booking_id, data_input, session):
    is_success, gw_deposit_open_account_td, request_data = await service_gw.deposit_open_account_td(
        current_user=current_user,
        data_input=data_input
    )
    session.add(
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=orjson_dumps(request_data),
            business_form_id=BUSINESS_FORM_OPEN_TD_OPEN_TD_ACCOUNT_PD,
            save_flag=True,
            created_at=now(),
            out_data=orjson_dumps(gw_deposit_open_account_td)
        ))
    )
    session.add(TransactionJob(**dict(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_OPEN_TD_ACCOUNT,
        complete_flag=is_success,
        error_code=gw_deposit_open_account_td.get('openTD_out').get('transaction_info').get('transaction_error_code'),
        error_desc=gw_deposit_open_account_td.get('openTD_out').get('transaction_info').get('transaction_error_msg'),
        created_at=now()
    )))
    return ReposReturn(data=gw_deposit_open_account_td)


async def repos_get_booking_account_by_booking(booking_id, session: Session):
    booking_accounts = session.execute(
        select(
            BookingAccount.td_account_id
        )
        .filter(BookingAccount.booking_id == booking_id)
    ).scalars().all()

    return ReposReturn(data=booking_accounts)


async def repos_get_customer_by_booking_account(td_accounts: List, session):
    customer = session.execute(
        select(
            Customer
        )
        .join(TdAccount, Customer.id == TdAccount.customer_id)
        .filter(
            TdAccount.id.in_(td_accounts)
        )
    ).scalar()
    return ReposReturn(data=customer)


async def repos_get_td_account(td_accounts: List, session):
    td_account = session.execute(
        select(
            TdAccount,
            TdAccountResign
        )
        .join(TdAccountResign, TdAccount.id == TdAccountResign.id)
        .filter(TdAccount.id.in_(td_accounts))
    ).all()
    return ReposReturn(data=td_account)
