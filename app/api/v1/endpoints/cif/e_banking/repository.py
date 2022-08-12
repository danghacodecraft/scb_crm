from pydantic import json
from sqlalchemy import delete, select
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
    EBankingReceiverNotificationRelationship, EBankingRegisterBalance,
    EBankingRegisterBalanceNotification, EBankingRegisterBalanceOption,
    TdAccount
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.account import AccountType
from app.utils.constant.cif import (
    BUSINESS_FORM_EB, BUSINESS_FORM_SMS_CASA, CIF_ID_TEST,
    EBANKING_ACCOUNT_TYPE_CHECKING
)
from app.utils.error_messages import (
    ERROR_CASA_ACCOUNT_NOT_EXIST, ERROR_CIF_ID_NOT_EXIST, ERROR_NO_DATA
)
from app.utils.functions import generate_uuid, now


@auto_commit
async def repos_save_e_banking(
        session: Session,
        data_insert: json,
        log_data: json,
        cif_id: str,
        created_by: str,
        history_datas: json
) -> ReposReturn:

    # 1. Customer đã có E-banking -> xóa dữ liệu cũ
    exist_ebank_info = session.execute(select(EBankingInfo).filter(EBankingInfo.customer_id == cif_id)).first()
    if exist_ebank_info:
        session.execute(delete(EBankingInfoAuthentication).filter(
            EBankingInfoAuthentication.e_banking_info_id == exist_ebank_info.EBankingInfo.id))

        session.delete(exist_ebank_info.EBankingInfo)

    # 2. Tạo dữ liệu mới
    ebank_info = data_insert['ebank_info']
    ebank_info.update({
        "note": None,
        "approval_status": None,
        "method_payment_fee_flag": None,
        "reset_password_flag": None,
        "active_account_flag": None,
        "account_payment_fee": None
    })
    ebank = EBankingInfo(**ebank_info)
    session.add(ebank)
    session.flush()

    ebank_info_authen_list = data_insert['ebank_info_authen_list']
    for ebank_info_authen in ebank_info_authen_list:
        ebank_info_authen.update({
            "e_banking_info_id": ebank.id
        })
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


@auto_commit
async def repos_save_sms_casa(
        cif_id: str,
        data_insert: dict,
        log_data: json,
        history_datas: json,
        created_by: str,
        session: Session
):
    # mapping dữ liệu cho các bảng
    registry_balance_item_list = []
    receiver_noti_relationship_item_list = []
    notify_code_item_list = []
    reg_balance_option_item_list = []
    for registry_balance_item in data_insert['registry_balance_items']:

        # 0. Validate casa_id
        account_number = registry_balance_item["casa_id"]

        casa_account = session.execute(
            select(
                CasaAccount.id
            ).filter(
                CasaAccount.id == account_number,
                CasaAccount.customer_id == cif_id
            )
        ).scalars().first()
        if not casa_account:
            return ReposReturn(is_error=True, msg=ERROR_CASA_ACCOUNT_NOT_EXIST)

        # 00. Kiểm tra casa_id có đăng ký reg_balance trước chưa -> xóa dữ liệu cũ.
        exist_registry_balance = session.execute(select(EBankingRegisterBalance).filter(EBankingRegisterBalance.account_id == account_number)).first()

        if exist_registry_balance:
            # 002
            session.execute(delete(EBankingReceiverNotificationRelationship).filter(
                EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id == exist_registry_balance.EBankingRegisterBalance.id))

            # 003
            session.execute(delete(EBankingRegisterBalanceNotification).filter(
                EBankingRegisterBalanceNotification.eb_reg_balance_id == exist_registry_balance.EBankingRegisterBalance.id))

            # 001
            session.delete(exist_registry_balance.EBankingRegisterBalance)

        # 01. Tạo mới dữ liệu SMS casa
        # a. registry_balance_item_list
        registry_balance_self_generate_id = generate_uuid()
        registry_balance = {
            "id": registry_balance_self_generate_id,
            "account_id": account_number,
            "e_banking_register_account_type": EBANKING_ACCOUNT_TYPE_CHECKING,
            "customer_id": cif_id,
            "name": registry_balance_item['main_phone_number_info'].customer_full_name,
            "mobile_number": registry_balance_item['main_phone_number_info'].main_phone_number,
            "full_name": registry_balance_item['main_phone_number_info'].customer_full_name
        }
        registry_balance_item_list.append(registry_balance)

        # b. receiver_noti_relationship_item_list
        for receiver_noti_relationship_item in registry_balance_item['receiver_noti_relationship_items']:
            receiver_noti_relationship = {
                "e_banking_register_balance_casa_id": registry_balance_self_generate_id,
                "mobile_number": receiver_noti_relationship_item.mobile_number,
                "relationship_type_id": receiver_noti_relationship_item.relationship_type_id,
                "full_name": receiver_noti_relationship_item.full_name,
            }
            receiver_noti_relationship_item_list.append(receiver_noti_relationship)

        # c. Bảng reg_balance_noti
        for notify_code_item in registry_balance_item['notify_code_list']:
            notify_code = {
                "eb_reg_balance_id": registry_balance_self_generate_id,
                "eb_notify_id": notify_code_item
            }
            notify_code_item_list.append(notify_code)

    # d. Bảng reg_balance_noti_option
    for reg_balance_option in data_insert['reg_balance_options']:
        reg_balance_option_item = {
            "customer_id": cif_id,
            "customer_contact_type_id": reg_balance_option,
            "e_banking_register_account_type": EBANKING_ACCOUNT_TYPE_CHECKING,
            "created_at": now()
        }
        reg_balance_option_item_list.append(reg_balance_option_item)

    # 1. Bảng reg_balance
    session.bulk_save_objects([
        EBankingRegisterBalance(**registry_balance_item) for registry_balance_item in registry_balance_item_list
    ])

    # 2. Bảng reg_noti_relationship
    session.bulk_save_objects([
        EBankingReceiverNotificationRelationship(**receiver_noti_relationship_item) for receiver_noti_relationship_item in receiver_noti_relationship_item_list
    ])

    # 3. Bảng reg_balance_noti
    session.bulk_save_objects([
        EBankingRegisterBalanceNotification(**notify_code_item) for notify_code_item in notify_code_item_list
    ])

    # 4. Bảng reg_balance_noti_option
    # 004, Xóa dữ liệu cũ
    session.execute(delete(EBankingRegisterBalanceOption).filter(
        EBankingRegisterBalanceOption.customer_id == cif_id))

    session.bulk_save_objects([
        EBankingRegisterBalanceOption(**reg_balance_option_item) for reg_balance_option_item in reg_balance_option_item_list
    ])

    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        history_datas=history_datas,
        session=session,
        customer_id=cif_id,
        business_form_id=BUSINESS_FORM_SMS_CASA
    )

    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    session.commit()

    return ReposReturn(data={
        "cif_id": cif_id,
        "created_at": now(),
        "created_by": created_by
    })


@auto_commit
async def repos_check_and_remove_exist_sms_casa(cif_id: str, session: Session):
    # Kiểm tra các tài khoản casa theo số cif
    casa_account_numbers = session.execute(
        select(
            CasaAccount.id
        ).filter(
            CasaAccount.customer_id == cif_id
        )
    ).scalars().all()

    for account_number in casa_account_numbers:
        # 00. Kiểm tra casa_id có đăng ký reg_balance trước chưa -> xóa dữ liệu cũ.
        exist_registry_balance = session.execute(
            select(EBankingRegisterBalance).filter(EBankingRegisterBalance.account_id == account_number)).first()

        if exist_registry_balance:
            # 002
            session.execute(delete(EBankingReceiverNotificationRelationship).filter(
                EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id == exist_registry_balance.EBankingRegisterBalance.id))

            # 003
            session.execute(delete(EBankingRegisterBalanceNotification).filter(
                EBankingRegisterBalanceNotification.eb_reg_balance_id == exist_registry_balance.EBankingRegisterBalance.id))

            # 001
            session.delete(exist_registry_balance.EBankingRegisterBalance)

    # 4. Bảng reg_balance_noti_option
    # 004, Xóa dữ liệu cũ
    session.execute(delete(EBankingRegisterBalanceOption).filter(
        EBankingRegisterBalanceOption.customer_id == cif_id))

    return ReposReturn(data=None)


async def repos_check_e_banking(cif_id: str, session: Session):
    e_banking_info = session.execute(select(EBankingInfo).filter(EBankingInfo.customer_id == cif_id)).first()
    return e_banking_info


async def repos_get_e_banking(cif_id: str, session: Session) -> ReposReturn:
    e_bank_info = session.execute(
        select(
            EBankingInfo.account_name,
            EBankingInfo.method_active_password_id,
            EBankingInfoAuthentication.method_authentication_id
        ).outerjoin(
            EBankingInfoAuthentication, EBankingInfoAuthentication.e_banking_info_id == EBankingInfo.id
        ).filter(
            EBankingInfo.customer_id == cif_id,
            EBankingInfo.approval_status == False  # noqa
        )
    ).all()

    if not e_bank_info:
        return ReposReturn(data=None)

    authentication_code_list = []
    for authentication_info in e_bank_info:
        if authentication_info.method_authentication_id:
            authentication_code_list.append(authentication_info.method_authentication_id)

    data = {
        "username": e_bank_info[0].account_name,
        "receive_password_code": e_bank_info[0].method_active_password_id,
        "authentication_code_list": authentication_code_list
    }

    return ReposReturn(data=data)


async def repos_get_sms_data(cif_id: str, session: Session) -> ReposReturn:
    # 1. Lấy casa_id, reg_balance
    casa_ids = session.execute(
        select(
            CasaAccount.id
        ).filter(
            CasaAccount.customer_id == cif_id
        )
    ).scalars().all()

    reg_balance_rows = session.execute(
        select(
            EBankingRegisterBalance.id.label('reg_balance_id'),
            EBankingRegisterBalance.full_name,
            EBankingRegisterBalance.mobile_number,
            EBankingRegisterBalance.account_id,

            EBankingReceiverNotificationRelationship.mobile_number.label('relationship_mobile_number'),
            EBankingReceiverNotificationRelationship.relationship_type_id.label('relationship_relationship_type_id'),
            EBankingReceiverNotificationRelationship.full_name.label('relationship_full_name'),

            EBankingRegisterBalanceNotification.eb_notify_id
        ).outerjoin(
            EBankingReceiverNotificationRelationship,
            EBankingReceiverNotificationRelationship.e_banking_register_balance_casa_id == EBankingRegisterBalance.id
        ).outerjoin(
            EBankingRegisterBalanceNotification,
            EBankingRegisterBalance.id == EBankingRegisterBalanceNotification.eb_reg_balance_id
        ).filter(
            EBankingRegisterBalance.account_id.in_(casa_ids),
            EBankingRegisterBalance.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING,
            EBankingRegisterBalance.approval_status == False  # noqa
        )
    ).all()

    # mapping receiver_noti_relationship_items
    reg_balance_id__receiver_noti_relationship_items = {}
    for reg_balance_row in reg_balance_rows:
        # TH không có đủ thông tin MQH, không hiển thị MQH này, điền list rỗng
        if reg_balance_row.relationship_mobile_number and reg_balance_row.relationship_full_name and reg_balance_row.relationship_relationship_type_id:
            receiver_noti_relationship_item = {
                "mobile_number": reg_balance_row.relationship_mobile_number,
                "full_name": reg_balance_row.relationship_full_name,
                "relationship_type_id": reg_balance_row.relationship_relationship_type_id
            }
            if reg_balance_row.reg_balance_id not in reg_balance_id__receiver_noti_relationship_items:
                reg_balance_id__receiver_noti_relationship_items[reg_balance_row.reg_balance_id] = [receiver_noti_relationship_item]
            elif receiver_noti_relationship_item not in reg_balance_id__receiver_noti_relationship_items[reg_balance_row.reg_balance_id]:
                reg_balance_id__receiver_noti_relationship_items[reg_balance_row.reg_balance_id].append(receiver_noti_relationship_item)
        # TH không có đủ thông tin MQH, không hiển thị MQH này, điền list rỗng
        else:
            reg_balance_id__receiver_noti_relationship_items[reg_balance_row.reg_balance_id] = []

    # mapping notify_code_list
    reg_balance_id__notify_code_list = {}
    for reg_balance_row in reg_balance_rows:
        # TH không có thông tin, điền list rỗng
        if reg_balance_row.eb_notify_id:
            if reg_balance_row.reg_balance_id not in reg_balance_id__notify_code_list:
                reg_balance_id__notify_code_list[reg_balance_row.reg_balance_id] = [reg_balance_row.eb_notify_id]
            elif reg_balance_row.eb_notify_id not in reg_balance_id__notify_code_list[reg_balance_row.reg_balance_id]:
                reg_balance_id__notify_code_list[reg_balance_row.reg_balance_id].append(reg_balance_row.eb_notify_id)
        # TH không có thông tin, điền list rỗng
        else:
            reg_balance_id__notify_code_list[reg_balance_row.reg_balance_id] = []

    # mapping for response data
    registry_balance_items = []
    checked_casa_ids = []
    for casa_id in casa_ids:
        reg_balance_item = {}
        for reg_balance_row in reg_balance_rows:
            if reg_balance_row.account_id == casa_id and casa_id not in checked_casa_ids:
                checked_casa_ids.append(casa_id)
                reg_balance_item = {
                    "casa_id": casa_id,
                    "main_phone_number_info": {
                        "main_phone_number": reg_balance_row.mobile_number,
                        "customer_full_name": reg_balance_row.full_name
                    },
                    "receiver_noti_relationship_items": reg_balance_id__receiver_noti_relationship_items.get(reg_balance_row.reg_balance_id),
                    "notify_code_list": reg_balance_id__notify_code_list.get(reg_balance_row.reg_balance_id)
                }

        if reg_balance_item:
            registry_balance_items.append(reg_balance_item)

    # 2. OTT-SMS
    sms_casa_reg_balance_options = session.execute(
        select(
            EBankingRegisterBalanceOption.customer_contact_type_id
        ).filter(
            EBankingRegisterBalanceOption.customer_id == cif_id,
            EBankingRegisterBalanceOption.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING
        )
    ).scalars().all()

    response_data = {
        "reg_balance_options": sms_casa_reg_balance_options,
        "registry_balance_items": registry_balance_items
    } if registry_balance_items else None  # Nếu không có đăng ký sms, trả None

    return ReposReturn(data=response_data)


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
