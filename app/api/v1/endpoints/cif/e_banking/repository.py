from pydantic import json
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingInfoAuthentication,
    EBankingReceiverNotificationRelationship, TdAccount
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountType
from app.utils.constant.cif import (
    BUSINESS_FORM_EB, BUSINESS_FORM_SMS_CASA, CIF_ID_TEST
)
from app.utils.error_messages import ERROR_CIF_ID_NOT_EXIST, ERROR_NO_DATA
from app.utils.functions import now


@auto_commit
async def repos_save_e_banking(
        session: Session,
        data_insert: json,
        log_data: json,
        cif_id: str,
        created_by: str,
        history_datas: json
) -> ReposReturn:
    ebank_info = data_insert['ebank_info']
    ebank_info.update(dict(
        note=None,
        ib_mb_flag=None,
        method_payment_fee_flag=None,
        reset_password_flag=None,
        active_account_flag=None,
        account_payment_fee=None
    ))
    ebank = EBankingInfo(**ebank_info)
    session.add(ebank)
    session.flush()

    ebank_info_authen_list = data_insert['ebank_info_authen_list']
    for ebank_info_authen in ebank_info_authen_list:
        ebank_info_authen.update(dict(
            e_banking_info_id=ebank.id
        ))
    session.bulk_save_objects([
        EBankingInfoAuthentication(**ebank_info_authen) for ebank_info_authen in ebank_info_authen_list
    ])
    session.flush()

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        history_datas=history_datas,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_EB
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


# @TODO: notification_type hiện giờ chưa đồng bộ , nên chưa cần nhập
@auto_commit
async def repos_save_sms_casa(
        cif_id: str,
        data_insert: dict,
        log_data: json,
        history_datas: json,
        created_by: str,
        session: Session
):
    sms_casa_list = []
    for mobile_number in data_insert['identity_phone_num_list']:
        sms_casa = dict(
            e_banking_register_balance_casa_id=data_insert['casa_account_id'],
            mobile_number=mobile_number.mobile_number,
            relationship_type_id=1,
            full_name=" "
        )
        sms_casa_list.append(sms_casa)
    session.bulk_save_objects([
        EBankingReceiverNotificationRelationship(**sms_casa) for sms_casa in sms_casa_list
    ])
    session.flush()

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        history_datas=history_datas,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_SMS_CASA
    )

    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


async def repos_check_e_banking(cif_id: str, session: Session):
    e_banking_info = session.execute(select(EBankingInfo).filter(EBankingInfo.customer_id == cif_id)).first()
    return e_banking_info


async def repos_get_e_banking(cif_id: str, session: Session) -> ReposReturn:
    e_bank_info = session.execute(
        select(
            EBankingInfo.account_name,
            EBankingInfo.method_active_password_id,
            EBankingInfoAuthentication.method_authentication_id
        ).join(
            EBankingInfoAuthentication, EBankingInfoAuthentication.e_banking_info_id == EBankingInfo.id
        ).filter(
            EBankingInfo.customer_id == cif_id
        )
    ).all()

    if not e_bank_info:
        return ReposReturn(data=None)

    data = dict(
        username=e_bank_info[0].account_name,
        receive_password_code=e_bank_info[0].method_active_password_id,
        authentication_code_list=[authentication_info.method_authentication_id for authentication_info in e_bank_info]
    )

    return ReposReturn(data=data)


async def repos_get_sms_data(cif_id: str, session: Session) -> ReposReturn:
    # Lấy TKTT theo số cif ảo
    casa_ids = session.execute(
        select(
            CasaAccount.id
        ).filter(
            CasaAccount.customer_id == cif_id
        )
    ).scalars().all()

    sms_casa_data = session.execute(
        select(
            EBankingReceiverNotificationRelationship.mobile_number,
            EBankingReceiverNotificationRelationship.relationship_type_id,
            EBankingReceiverNotificationRelationship.full_name,
            EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id
        ).filter(
            EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id.in_(casa_ids)
        )
    ).all()

    if not sms_casa_data:
        return ReposReturn(data=None)

    sms_casa_info_list = []

    for casa_id in casa_ids:
        sms_casa_info = dict(
            casa_id=casa_id,
            sms_casa_items=[]
        )
        for sms_casa in sms_casa_data:
            if sms_casa.e_banking_register_balance_casa_id == casa_id:
                sms_casa_info["sms_casa_items"].append(dict(
                    full_name=sms_casa.full_name,
                    mobile_number=sms_casa.mobile_number,
                    relationship_type_id=sms_casa.relationship_type_id
                ))

        sms_casa_info_list.append(sms_casa_info)
    print(sms_casa_info_list)
    return ReposReturn(data=sms_casa_info_list)


DETAIL_RESET_PASSWORD_E_BANKING_DATA = {
    "personal_customer_information": {
        "id": "1234567",
        "cif_number": "1324567",
        "customer_classification": {
            "id": "1",
            "code": "CA_NHAN",
            "name": "Cá nhân"
        },
        "avatar_url": "example.com/example.jpg",
        "full_name": "TRAN MINH HUYEN",
        "gender": {
            "id": "1",
            "code": "NU",
            "name": "Nữ"
        },
        "email": "nhuxuanlenguyen153@gmail.com",
        "mobile_number": "0896524256",
        "identity_number": "079197005869",
        "place_of_issue": {
            "id": "1",
            "code": "HCM",
            "name": "TPHCM"
        },
        "issued_date": "2021-02-18",
        "expired_date": "2021-02-18",
        "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
        "e_banking_reset_password_method": [
            {
                "id": "1",
                "code": "SMS",
                "name": "SMS",
                "checked_flag": False
            },
            {
                "id": "2",
                "code": "EMAIL",
                "name": "EMAIL",
                "checked_flag": True
            }
        ],
        "e_banking_account_name": "huyentranminh"
    },
    "question": {
        "basic_question_1": {
            "branch_of_card": {
                "id": "123",
                "code": "MASTERCARD",
                "name": "Mastercard",
                "color": {
                    "id": "123",
                    "code": "YELLOW",
                    "name": "Vàng"
                }
            },
            "sub_card_number": 2,
            "mobile_number": "0897528556",
            "branch": {
                "id": "0897528556",
                "code": "HO",
                "name": "Hội Sở"
            },
            "method_authentication": {
                "id": "1",
                "code": "SMS",
                "name": "SMS"
            },
            "e_banking_account_name": "huyentranminh"
        },
        "basic_question_2": {
            "last_four_digits": "1234",
            "credit_limit": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "email": "huyentranminh126@gmail.com",
            "secret_question_or_personal_relationships": [
                {
                    "customer_relationship": {
                        "id": "1",
                        "code": "MOTHER",
                        "name": "Mẹ"
                    },
                    "mobile_number": "0867589623"
                }
            ],
            "automatic_debit_status": "",
            "transaction_method_receiver": {
                "id": "1",
                "code": "EMAIL",
                "name": "Email"
            }
        },
        "advanced_question": {
            "used_limit_of_credit_card": {
                "value": "20000000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "nearest_3d_secure": {
                "business_partner": {
                    "id": "1",
                    "code": "GRAB",
                    "name": "Grab"
                },
                "value": "125000",
                "currency": {
                    "id": "1",
                    "code": "VND",
                    "name": "Việt Nam Đồng"
                }
            },
            "one_of_two_nearest_successful_transaction": "",
            "nearest_successful_login_time": ""
        }
    },
    "document_url": "example.com/example.pdf",
    "result": {
        "confirm_current_transaction_flag": True,
        "note": "Trả lời đầy đủ các câu hỏi"
    }
}


async def repos_get_payment_accounts(cif_id: str, session: Session) -> ReposReturn:
    payment_accounts = session.execute(
        select(
            CasaAccount,
            AccountType
        ).join(AccountType, CasaAccount.acc_type_id == AccountType.id).filter(CasaAccount.customer_id == cif_id)
    ).all()

    if not payment_accounts:
        return ReposReturn(
            is_error=True,
            msg=ERROR_NO_DATA,
            detail="Create payment account (III. Tài khoản thanh toán) before get data",
            loc=f"cif_id: {cif_id}"
        )

    return ReposReturn(data=payment_accounts)


async def repos_get_detail_reset_password(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=DETAIL_RESET_PASSWORD_E_BANKING_DATA)


async def repos_balance_saving_account_data(cif_id: str, session: Session) -> ReposReturn:
    # cif_number_saving_account = session.execute(
    #     select(
    #         Customer.cif_number
    #     ).filter(Customer.id == cif_id)
    # ).scalar()
    # saving_account = None
    # if cif_number_saving_account:
    #     saving_account = await service_soa.deposit_account_from_cif(saving_cif_number=cif_number_saving_account)

    saving_accounts = session.execute(
        select(
            Customer,
            TdAccount
        ).filter(Customer.id == cif_id)
    ).all()

    if not saving_accounts:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    response_datas = [
        {
            "id": td_account.id,
            "account_number": td_account.td_account_number,
            "name": customer.full_name_vn,
            "checked_flag": td_account.active_flag

        } for customer, td_account in saving_accounts]

    return ReposReturn(data=response_datas)


async def repos_get_detail_reset_password_teller(cif_id: str) -> ReposReturn:
    if cif_id != CIF_ID_TEST:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data={
        "personal_customer_information": {
            "id": "1234567",
            "cif_number": "1324567",
            "customer_classification": {
                "id": "1",
                "code": "CANHAN",
                "name": "Cá nhân"
            },
            "avatar_url": "example.com/example.jpg",
            "full_name": "TRAN MINH HUYEN",
            "gender": {
                "id": "1",
                "code": "NU",
                "name": "Nữ"
            },
            "email": "nhuxuanlenguyen153@gmail.com",
            "mobile_number": "0896524256",
            "identity_number": "079197005869",
            "place_of_issue": {
                "id": "1",
                "code": "HCM",
                "name": "TPHCM"
            },
            "issued_date": "2019-02-01",
            "expired_date": "2032-03-02",
            "address": "144 Nguyễn Thị Minh Khai, Phường Bến Nghé, Quận 1, TPHCM",
            "e_banking_reset_password_method": [
                {
                    "id": "1",
                    "code": "SMS",
                    "name": "SMS",
                    "checked_flag": False
                },
                {
                    "id": "2",
                    "code": "EMAIL",
                    "name": "EMAIL",
                    "checked_flag": True
                }
            ],
            "e_banking_account_name": "huyentranminh"
        },
        "document": {
            "id": "1",
            "name": "Biểu mẫu đề nghị cấp lại mật khẩu Ebanking",
            "url": "https://example.com/abc/pdf",
            "version": "1.0",
            "created_by": "Nguyễn Phúc",
            "created_at": "2020-02-01 08:40",
            "active_flag": True
        }
    })
