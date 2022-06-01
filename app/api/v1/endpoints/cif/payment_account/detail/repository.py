import json

from sqlalchemy import select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw, service_soa
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountStructureType, AccountType
)
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import (
    BUSINESS_FORM_TKTT_CTTKTT, DROPDOWN_NONE_DICT
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_CALL_SERVICE_SOA, ERROR_INVALID_NUMBER,
    ERROR_NO_DATA, MESSAGE_STATUS
)
from app.utils.functions import dropdown, is_valid_number, now


async def repos_detail_payment_account(cif_id: str, session: Session) -> ReposReturn:
    account_structure_type_level_2 = aliased(AccountStructureType, name='account_structure_type_level_2')
    account_structure_type_level_1 = aliased(AccountStructureType, name='account_structure_type_level_1')
    detail = session.execute(
        select(
            CasaAccount,
            Currency,
            AccountClass,
            AccountType,
            AccountStructureType,
            account_structure_type_level_2,
            account_structure_type_level_1,
        )
        .join(Currency, CasaAccount.currency_id == Currency.id)
        .join(AccountClass, CasaAccount.acc_class_id == AccountClass.id)
        .join(AccountType, CasaAccount.acc_type_id == AccountType.id)
        .outerjoin(AccountStructureType, CasaAccount.acc_structure_type_id == AccountStructureType.id)
        .outerjoin(
            account_structure_type_level_2,
            AccountStructureType.parent_id == account_structure_type_level_2.id
        )
        .outerjoin(
            account_structure_type_level_1,
            account_structure_type_level_2.parent_id == account_structure_type_level_1.id
        )
        .filter(CasaAccount.customer_id == cif_id)
    ).first()

    if not detail:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, detail=MESSAGE_STATUS[ERROR_NO_DATA])

    account_structure_type_level_1 = detail.account_structure_type_level_1
    account_structure_type_level_2 = detail.account_structure_type_level_2
    account_structure_type_level_3 = detail.AccountStructureType

    return ReposReturn(data={
        "self_selected_account_flag": detail.CasaAccount.self_selected_account_flag,
        "currency": dropdown(detail.Currency),
        "account_type": dropdown(detail.AccountType),
        "account_class": dropdown(detail.AccountClass),
        "account_structure_type_level_1": dropdown(account_structure_type_level_1)
        if account_structure_type_level_1 else DROPDOWN_NONE_DICT,
        "account_structure_type_level_2": dropdown(account_structure_type_level_2)
        if account_structure_type_level_2 else DROPDOWN_NONE_DICT,
        "account_structure_type_level_3": dropdown(account_structure_type_level_3)
        if account_structure_type_level_3 else DROPDOWN_NONE_DICT,
        "casa_account_number": detail.CasaAccount.casa_account_number,
        "account_salary_organization_account": detail.CasaAccount.acc_salary_org_acc,
        "account_salary_organization_name": detail.CasaAccount.acc_salary_org_name
    })


@auto_commit
async def repos_save_payment_account(
        cif_id: str,
        data_insert: dict,
        log_data: json,
        history_datas: json,
        created_by: str,
        session: Session,
        is_created: bool
):
    # Tạo mới
    if is_created:
        session.add(CasaAccount(**data_insert))
        is_success, booking_response = await write_transaction_log_and_update_booking(
            log_data=log_data,
            history_datas=history_datas,
            session=session,
            customer_id=cif_id,
            business_form_id=BUSINESS_FORM_TKTT_CTTKTT
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=booking_response['msg'])
    # Cập nhật
    else:
        session.execute(
            update(CasaAccount).where(
                CasaAccount.customer_id == cif_id
            ).values(**data_insert)
        )
        is_success, booking_response = await write_transaction_log_and_update_booking(
            log_data=log_data,
            history_datas=history_datas,
            session=session,
            customer_id=cif_id,
            business_form_id=BUSINESS_FORM_TKTT_CTTKTT
        )
        if not is_success:
            return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


########################################################################################################################
# Others
########################################################################################################################
async def repos_check_casa_account(cif_id: str, session: Session):
    casa_account = session.execute(
        select(
            CasaAccount
        ).filter(
            CasaAccount.customer_id == cif_id
        )
    ).scalars().first()

    return ReposReturn(data=casa_account)


async def repos_check_exist_casa_account_number(casa_account_number: str, session: Session):
    """
        Kiểm tra số tài khoản thanh toán có tồn tại hay không
    """
    is_success, check_exist_info = await service_soa.retrieve_current_account_casa(
        casa_account_number=casa_account_number
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_SOA, detail=check_exist_info["message"])

    return ReposReturn(data=check_exist_info)


async def repos_gw_check_exist_casa_account_number(
        casa_account_number: str,
        current_user: AuthResponse):
    is_success, check_exist_casa_account_number = await service_gw.check_exist_casa_account_number(
        casa_account_number=casa_account_number, current_user=current_user.user_info
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc='check_exist_casa_account_number',
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(check_exist_casa_account_number)
        )
    return ReposReturn(data=check_exist_casa_account_number)


async def repos_get_casa_account_from_soa(casa_account_number: str, loc: str):
    """
    Lấy thông tin tài khoản thanh toán bằng số tài khoản thanh toán
    """
    if not is_valid_number(casa_account_number):
        return ReposReturn(
            is_error=True,
            msg=ERROR_INVALID_NUMBER,
            detail=MESSAGE_STATUS[ERROR_INVALID_NUMBER],
            loc=loc
        )

    is_success, account_salary_organization_response = await service_soa.retrieve_current_account_casa(
        casa_account_number=casa_account_number
    )

    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_SOA,
                           detail=MESSAGE_STATUS[ERROR_CALL_SERVICE_SOA])

    return ReposReturn(data=account_salary_organization_response)
