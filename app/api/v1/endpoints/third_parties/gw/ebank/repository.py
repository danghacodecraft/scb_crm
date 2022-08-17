from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW, ERROR_NO_DATA


async def repos_gw_get_retrieve_ebank_by_cif_number(
        cif_num: str, current_user
):
    current_user = current_user.user_info
    is_success, retrieve_ebank = await service_gw.get_retrieve_ebank_td(
        cif_num=cif_num, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_ebank_from_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(retrieve_ebank)
        )

    return ReposReturn(data=retrieve_ebank)


async def repos_gw_get_retrieve_internet_banking_by_cif_number(
        cif_num: str, current_user
):
    current_user = current_user.user_info
    is_success, retrieve_internet_banking = await service_gw.get_retrieve_internet_banking(
        cif_num=cif_num, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_retrieve_internet_banking",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(retrieve_internet_banking)
        )

    return ReposReturn(data=retrieve_internet_banking)


async def repos_gw_get_open_ib(
    request,
    current_user
):
    current_user = current_user.user_info
    is_success, open_ib = await service_gw.get_open_ib(
        request=request, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_open_ib",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(open_ib)
        )

    return ReposReturn(data=open_ib)


async def repos_get_e_banking_from_db_by_cif_id(cif_id: str, session: Session):
    e_banking_row = session.execute(
        select(
            EBankingInfo.id,
            EBankingInfo.customer_id,
            EBankingInfo.account_name,
            EBankingInfo.method_active_password_id
        )
        .filter(
            EBankingInfo.customer_id == cif_id,
            EBankingInfo.approval_status == 0
        )
    ).first()

    # Không tìm thấy thông tin Ebanking có thể do khách hàng không đăng ký
    if not e_banking_row:
        return ReposReturn(data=None)

    e_banking = {
        "id": e_banking_row.id,
        "customer_id": e_banking_row.customer_id,
        "account_name": e_banking_row.account_name,
        "method_active_password_id": e_banking_row.method_active_password_id
    }

    e_banking_authen = session.execute(
        select(
            EBankingInfoAuthentication.method_authentication_id,
        )
        .filter(EBankingInfoAuthentication.e_banking_info_id == e_banking["id"])
    ).scalars().all()

    e_banking["authentication_info_list"] = []
    if e_banking_authen:
        e_banking["authentication_info_list"] = e_banking_authen

    return ReposReturn(data=e_banking)


async def repos_get_sms_casa_mobile_number_from_db_by_cif_id(cif_id, session: Session):
    # Quá trình mở cif chỉ một tài khoản Casa
    casa_id = session.execute(
        select(
            CasaAccount.id,
        )
        .filter(CasaAccount.customer_id == cif_id)
    ).scalars().first()

    if not casa_id:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="repos_get_sms_casa_from_db_by_cif_id -> casa_id")

    balance_and_relationship_info = session.execute(
        select(
            EBankingRegisterBalance.id.label('reg_balance_id'),
            EBankingReceiverNotificationRelationship.mobile_number
        ).outerjoin(
            EBankingReceiverNotificationRelationship,
            EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id == EBankingRegisterBalance.id
        )
        .filter(
            EBankingRegisterBalance.account_id == casa_id,
            EBankingRegisterBalance.approval_status == 0
        )
    ).all()

    balance_id__relationship_mobile_numbers = {}
    for item in balance_and_relationship_info:
        if item['reg_balance_id'] not in balance_id__relationship_mobile_numbers:
            balance_id__relationship_mobile_numbers[item['reg_balance_id']] = []

        balance_id__relationship_mobile_numbers[item['reg_balance_id']].append(item.mobile_number)

    if not balance_id__relationship_mobile_numbers:
        return ReposReturn(data=None)

    return ReposReturn(data=balance_id__relationship_mobile_numbers)
