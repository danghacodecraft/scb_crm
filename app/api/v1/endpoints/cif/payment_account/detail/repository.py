import json
from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountStructureType, AccountType
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.others import Currency
from app.utils.constant.cif import BUSINESS_FORM_TKTT_CTTKTT
from app.utils.error_messages import ERROR_CALL_SERVICE_GW
from app.utils.functions import now


async def repos_get_detail_payment_account(cif_id: str, session: Session) -> ReposReturn:
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
            AddressCountry
        )
        .join(Currency, CasaAccount.currency_id == Currency.id)
        .outerjoin(AddressCountry, Currency.country_code == AddressCountry.id)
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

    return ReposReturn(data=detail)


async def repos_get_detail_payment_accounts_by_account_ids(casa_account_ids: List[str], session: Session) -> ReposReturn:
    account_structure_type_level_2 = aliased(AccountStructureType, name='account_structure_type_level_2')
    account_structure_type_level_1 = aliased(AccountStructureType, name='account_structure_type_level_1')
    casa_accounts = session.execute(
        select(
            CasaAccount,
            Currency,
            AccountClass,
            AccountType,
            AccountStructureType,
            account_structure_type_level_2,
            account_structure_type_level_1,
            AddressCountry
        )
        .join(Currency, CasaAccount.currency_id == Currency.id)
        .outerjoin(AddressCountry, Currency.country_code == AddressCountry.id)
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
        .filter(
            CasaAccount.id.in_(casa_account_ids),
            # Bypass account đã approve
            CasaAccount.casa_account_number.is_(None)
        )
    ).all()

    return ReposReturn(data=casa_accounts)


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
