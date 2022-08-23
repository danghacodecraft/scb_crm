from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.utils.error_messages import ERROR_CALL_SERVICE_GW, ERROR_NO_DATA
from app.utils.mapping import mapping_authentication_code_core_to_crm


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


@auto_commit
async def repos_check_and_remove_exist_ebank(session: Session, cif_id: str):
    # Xóa ebank theo số cif
    exist_ebank_info = session.execute(
        select(EBankingInfo).filter(
            EBankingInfo.customer_id == cif_id,
        )
    ).first()

    if exist_ebank_info:
        session.delete(exist_ebank_info.EBankingInfo)

    return ReposReturn(data=None)


async def repos_pull_e_banking_from_gw_cif_number_and_return_is_exist_ebank(
        cif_id: str,
        cif_number: str,
        current_user,
        session: Session
) -> ReposReturn:
    internet_banking_info = await repos_gw_get_retrieve_internet_banking_by_cif_number(cif_number, current_user)
    if internet_banking_info.is_error:
        return ReposReturn(
            is_error=True,
            msg=internet_banking_info.msg,
            loc=internet_banking_info.loc,
            detail=internet_banking_info.detail
        )
    e_banking = internet_banking_info.data['retrieveIBInfoByCif_out']['data_output']['ebank_ibmb_info']
    if not e_banking:
        return ReposReturn(data=False)
    else:
        # mapping data ebank
        e_banking = e_banking[0]
        authentication_code_list = []
        for ebank_ibmb_authentication_info in e_banking['ebank_ibmb_authentication_info_list']:
            core_authentication_code = ebank_ibmb_authentication_info['ebank_ibmb_authentication_info_item']['authentication_code']
            authentication_code_list.append(mapping_authentication_code_core_to_crm(core_authentication_code))

        ebank_info = {
            "customer_id": cif_id,
            "account_name": e_banking['ebank_ibmb_username'],
            "method_active_password_id": e_banking['ebank_ibmb_notify_mode'],
            "note": None,
            "approval_status": True,
            "method_payment_fee_flag": None,
            "reset_password_flag": None,
            "active_account_flag": None,
            "account_payment_fee": None
        }
        ebank_info_authen_list = [{
            "method_authentication_id": authentication_code
        } for authentication_code in authentication_code_list]

        # Override thông tin ebank trên Db
        if cif_id:
            # 1. Customer đã có E-banking -> xóa dữ liệu cũ
            await repos_check_and_remove_exist_ebank(
                cif_id=cif_id,
                session=session
            )

        # 2. Tạo dữ liệu mới
        ebank_info = ebank_info
        ebank = EBankingInfo(**ebank_info)
        session.add(ebank)
        session.flush()

        for ebank_info_authen in ebank_info_authen_list:
            ebank_info_authen.update({
                "e_banking_info_id": ebank.id
            })
        session.bulk_save_objects([
            EBankingInfoAuthentication(**ebank_info_authen) for ebank_info_authen in ebank_info_authen_list
        ])
        session.commit()

    return ReposReturn(data=True)


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


async def repos_get_e_banking_from_db_by_cif_number(cif_number: str, session: Session):
    e_banking_row = session.execute(
        select(
            EBankingInfo.id,
            EBankingInfo.customer_id,
            EBankingInfo.account_name,
            EBankingInfo.method_active_password_id
        ).join(
            Customer, Customer.cif_number == cif_number
        ).filter(
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
