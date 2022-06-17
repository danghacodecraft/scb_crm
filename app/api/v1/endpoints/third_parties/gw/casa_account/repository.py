from typing import List

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWAccountInfoCloseCasaRequest
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import TransactionJob
from app.utils.constant.approval import BUSINESS_JOB_CODE_OPEN_CASA
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_APPROVED
from app.utils.constant.cif import BUSINESS_FORM_OPEN_CASA_PD
from app.utils.constant.gw import (
    GW_TRANSACTION_NAME_COLUMN_CHART, GW_TRANSACTION_NAME_PIE_CHART,
    GW_TRANSACTION_NAME_STATEMENT
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW, ERROR_CASA_ACCOUNT_APPROVED
from app.utils.functions import generate_uuid, now, orjson_dumps


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
    # from_date: date,
    # to_date: date
):
    is_success, gw_report_column_chart_casa_account_info = await service_gw.get_report_history_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_COLUMN_CHART,
        # from_date=from_date,
        # to_date=to_date
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
    # from_date: date,
    # to_date: date
):
    is_success, gw_report_history_account_info = await service_gw.get_report_statement_casa_account(
        current_user=current_user,
        account_number=account_number,
        transaction_name=GW_TRANSACTION_NAME_STATEMENT,
        # from_date=from_date,
        # to_date=to_date
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_report_statement_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_report_history_account_info)
        )

    return ReposReturn(data=gw_report_history_account_info)


async def repos_gw_open_casa_account(
    cif_number: str,
    self_selected_account_flag: bool,
    casa_account_info,
    booking_parent_id: str,
    session: Session,
    current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, gw_open_casa_account_info, form_data = await service_gw.get_open_casa_account(
        cif_number=cif_number,
        self_selected_account_flag=self_selected_account_flag,
        casa_account_info=casa_account_info,
        current_user=current_user
    )
    await repos_add_business_form_and_transaction_job(
        booking_id=booking_parent_id,
        business_form_id=BUSINESS_FORM_OPEN_CASA_PD,
        form_data=form_data,
        gw_response=gw_open_casa_account_info,
        is_success=is_success,
        session=session
    )

    return is_success, gw_open_casa_account_info


async def repos_gw_get_close_casa_account(
        account_info: GWAccountInfoCloseCasaRequest,
        p_blk_closure,
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, gw_close_casa_account_info = await service_gw.get_close_casa_account(
        account_info=account_info,
        p_blk_closure=p_blk_closure,
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_close_casa_account",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(gw_close_casa_account_info)
        )

    return ReposReturn(data=gw_close_casa_account_info)


async def repos_open_casa_get_casa_account_infos(
    casa_account_ids: List[str],
    session: Session
):
    casa_account_infos = session.execute(
        select(
            CasaAccount
        )
        .filter(CasaAccount.id.in_(casa_account_ids))
    ).scalars().all()
    return ReposReturn(data=casa_account_infos)


async def repos_add_business_form_and_transaction_job(
    booking_id: str,
    business_form_id: str,
    form_data: dict,
    session: Session,
    gw_response,
    is_success: bool,
):
    history_datas = []
    error_code = None
    error_desc = None
    if not is_success:
        transaction_info = gw_response['openCASA_out']['transaction_info']
        error_code = transaction_info['transaction_error_code']
        error_desc = transaction_info['transaction_error_msg']

    session.add_all([
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_OPEN_CASA,
            complete_flag=is_success,
            error_code=error_code,
            error_desc=error_desc,
            created_at=now()
        )),
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            business_form_id=business_form_id,
            save_flag=True,
            created_at=now(),
            form_data=orjson_dumps(form_data),
            log_data=orjson_dumps(history_datas)
        ))
    ])

    session.commit()
    return True


@auto_commit
async def repos_update_casa_account_to_approved(
    update_casa_accounts: List,
    session: Session
):
    session.bulk_update_mappings(CasaAccount, update_casa_accounts)

    return ReposReturn(data=True)


async def repos_check_casa_account_approved(casa_account_ids: List, session: Session):
    casa_account_status_approved_ids = session.execute(
        select(
            CasaAccount.id
        ).filter(and_(
            CasaAccount.id.in_(casa_account_ids),
            CasaAccount.approve_status == CASA_ACCOUNT_STATUS_APPROVED
        ))
    ).scalars().all()

    if casa_account_status_approved_ids:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CASA_ACCOUNT_APPROVED,
            loc=f'casa_account_ids: {casa_account_status_approved_ids}'
        )

    return ReposReturn(data=casa_account_status_approved_ids)
