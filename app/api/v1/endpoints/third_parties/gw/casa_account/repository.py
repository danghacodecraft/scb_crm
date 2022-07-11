from datetime import date
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_casa_account_by_account_number
)
from app.api.v1.endpoints.user.schema import AuthResponse, UserInfoResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import BookingBusinessForm
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import TransactionJob
from app.utils.constant.approval import BUSINESS_JOB_CODE_OPEN_CASA
from app.utils.constant.casa import CASA_ACCOUNT_STATUS_APPROVED
from app.utils.constant.cif import (
    BUSINESS_FORM_CLOSE_CASA_PD, BUSINESS_FORM_OPEN_CASA_PD
)
from app.utils.constant.gw import (
    GW_TRANSACTION_NAME_COLUMN_CHART, GW_TRANSACTION_NAME_PIE_CHART,
    GW_TRANSACTION_NAME_STATEMENT, GW_TRANSACTION_RESPONSE_STATUS_SUCCESS
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CASA_ACCOUNT_APPROVED
)
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


@auto_commit
async def repos_gw_get_close_casa_account(
        current_user,
        request_data_gw: list,
        booking_id,
        session
):
    response_data = []
    account_number = []
    current_user = current_user.user_info
    for item in request_data_gw:

        is_success, gw_close_casa_account, request_data = await service_gw.get_close_casa_account(
            data_input=item,
            current_user=current_user
        )
        # lưu form data request GW
        session.add(
            BookingBusinessForm(**dict(
                booking_id=booking_id,
                form_data=orjson_dumps(request_data),
                business_form_id=BUSINESS_FORM_CLOSE_CASA_PD,
                save_flag=True,
                created_at=now(),
                log_data=orjson_dumps(gw_close_casa_account)
            ))
        )
        casa_account_number = item.get('account_info').get('account_num')
        casa_account = await repos_get_casa_account_by_account_number(casa_account_number, session)

        if is_success:
            close_casa = gw_close_casa_account['closeCASA_out']['transaction_info']
            if close_casa.get('transaction_error_code') == GW_TRANSACTION_RESPONSE_STATUS_SUCCESS:
                account_number.append({
                    "id": casa_account.data,
                    "casa_account_number": casa_account_number,
                    "acc_active_flag": False
                })
            response_data.append({
                "transaction": {
                    "account_number": casa_account_number,
                    "code": close_casa.get('transaction_error_code'),
                    "msg": close_casa.get('transaction_error_msg')
                }
            })
        else:
            response_data.append({
                "transaction": {
                    "account_number": casa_account_number,
                    "code": ERROR_CALL_SERVICE_GW,
                    "msg": ERROR_CALL_SERVICE_GW
                }
            })

    # đóng trạng thái hoạt động của tài khoản
    session.bulk_update_mappings(CasaAccount, account_number)

    return ReposReturn(data=response_data)


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


async def repos_gw_get_tele_transfer(current_user: UserInfoResponse, data_input):
    is_success, tele_transfer = await service_gw.get_tele_transfer(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_tele_transfer",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(tele_transfer)
        )

    return ReposReturn(data=tele_transfer)


async def repos_gw_get_retrieve_ben_name_by_account_number(current_user: UserInfoResponse, data_input):
    is_success, ben_name = await service_gw.get_ben_name_by_account_number(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_retrieve_ben_name_by_account_number",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(ben_name)
        )
    return ReposReturn(data=ben_name)


async def repos_gw_get_retrieve_ben_name_by_card_number(current_user: UserInfoResponse, data_input):
    is_success, ben_name = await service_gw.get_ben_name_by_card_number(
        current_user=current_user,
        data_input=data_input
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_gw_get_retrieve_ben_name_by_card_number",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(ben_name)
        )
    return ReposReturn(data=ben_name)
