from typing import List

from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.cif.debit_card.repository import repos_debit_card
from app.api.v1.endpoints.cif.payment_account.detail.repository import (
    repos_get_detail_payment_account,
    repos_get_detail_payment_accounts_by_account_ids
)
from app.api.v1.endpoints.third_parties.gw.ebank.repository import (
    repos_get_e_banking_from_db_by_cif_id,
    repos_get_sms_casa_mobile_number_from_db_by_cif_id
)
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerProfessional
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity, CustomerIdentityImage
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.debit_card.model import DebitCard
from app.third_parties.oracle.models.cif.e_banking.model import (
    EBankingInfo, EBankingRegisterBalance
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.other_information.model import (
    CustomerEmployee
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Currency, TransactionJob
)
from app.utils.constant.approval import (
    BUSINESS_JOB_CODE_CASA_INFO, BUSINESS_JOB_CODE_CIF_INFO,
    BUSINESS_JOB_CODE_DEBIT_CARD, BUSINESS_JOB_CODE_E_BANKING,
    BUSINESS_JOB_CODE_INIT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_OPEN_CIF_PD, CUSTOMER_COMPLETED_FLAG, CUSTOMER_TYPE_ORGANIZE,
    IMAGE_TYPE_FACE, RESIDENT_ADDRESS_CODE, STAFF_TYPE_BUSINESS_CODE
)
from app.utils.constant.debit_card import (
    CRM_CUST_TITLE_MR, CRM_DELIVERY_ADDRESS_FLAG_FALSE, GW_CUST_TITLE_MR,
    GW_CUST_TITLE_MRS, GW_DEFAULT_ATM_CARD_ACCOUNT_PROVIDER,
    GW_DEFAULT_CARD_AUTO_RENEW, GW_DEFAULT_CARD_BILL_OPTION,
    GW_DEFAULT_CARD_RELATION_TO_PRIMARY,
    GW_DEFAULT_CARD_STATEMENT_DELIVERY_OPTION, GW_DEFAULT_NORMAL,
    GW_DEFAULT_QUICK, MAIN_CARD
)
from app.utils.constant.gw import (
    GW_AUTO, GW_CUSTOMER_TYPE_B, GW_CUSTOMER_TYPE_I, GW_DATE_FORMAT,
    GW_DEFAULT_CUSTOMER_CATEGORY, GW_DEFAULT_KHTC_DOI_TUONG, GW_DEFAULT_NO,
    GW_DEFAULT_TYPE_ID, GW_DEFAULT_VALUE, GW_DEFAULT_YES, GW_LANGUAGE,
    GW_LOCAL_CODE, GW_NO_AGREEMENT_FLAG, GW_NO_MARKETING_FLAG, GW_SELECT,
    GW_UDF_NAME, GW_YES, GW_YES_AGREEMENT_FLAG
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_NO_DATA, ERROR_OPEN_CIF
)
from app.utils.functions import (
    date_to_string, generate_uuid, now, orjson_dumps
)
from app.utils.vietnamese_converter import split_name


async def repos_gw_get_customer_info_list(
        cif_number: str,
        identity_number: str,
        mobile_number: str,
        full_name: str,
        current_user: AuthResponse
):
    current_user = current_user.user_info
    is_success, customer_infos = await service_gw.get_customer_info_list(
        cif_number=cif_number,
        identity_number=identity_number,
        mobile_number=mobile_number,
        full_name=full_name,
        current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_customer_info_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(customer_infos)
        )

    return ReposReturn(data=customer_infos)


async def repos_get_customer_ids_from_cif_numbers(cif_numbers: List, session: Session):
    customer_ids = session.execute(
        select(
            Customer.id,
            Customer.cif_number
        ).filter(
            Customer.cif_number.in_(cif_numbers)
        )
    ).all()

    return ReposReturn(data=customer_ids)


async def repos_gw_get_customer_info_detail(
        cif_number: str, current_user: AuthResponse,
        loc: str = "get_customer_info_detail"
):
    current_user = current_user.user_info
    is_success, customer_info = await service_gw.get_customer_info_detail(
        customer_cif_number=cif_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc=loc,
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(customer_info)
        )

    return ReposReturn(data=customer_info)


async def repos_gw_get_co_owner(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, co_owner = await service_gw.get_co_owner(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_co_owner_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(co_owner)
        )

    return ReposReturn(data=co_owner)


async def repos_gw_get_authorized(
        account_number: str, current_user
):
    current_user = current_user.user_info
    is_success, authorized = await service_gw.get_authorized(
        account_number=account_number, current_user=current_user
    )
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="get_authorized_list",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(authorized)
        )

    return ReposReturn(data=authorized)


@auto_commit
async def repos_gw_open_cif(
        booking_id: str,
        customer_info: dict,
        account_info: dict,
        current_user,
        transaction_jobs: List,
        session: Session
):
    data_input = {
        "customer_info": customer_info,
        "account_info": account_info
    }

    is_success, response_data = await service_gw.open_cif(
        data_input=data_input,
        current_user=current_user
    )
    booking_business_form_id = generate_uuid()

    saving_booking_business_form = {
        "booking_id": booking_id,
        "business_form_id": BUSINESS_FORM_OPEN_CIF_PD,
        "booking_business_form_id": booking_business_form_id,
        "save_flag": True,
        "is_success": True,
        "created_at": now(),
        "form_data": orjson_dumps(data_input),
        "out_data": orjson_dumps(response_data),
    }
    if not is_success:
        saving_booking_business_form.update({
            "is_success": False
        })
        for transaction_job in transaction_jobs:
            transaction_job.update({
                "complete_flag": False,
                "error_code": ERROR_OPEN_CIF
            })

    session.add(BookingBusinessForm(**saving_booking_business_form))
    session.bulk_save_objects(
        TransactionJob(**transaction_job) for transaction_job in transaction_jobs
    )

    return ReposReturn(data=(is_success, response_data))


@auto_commit
async def repos_update_cif_number_customer(
        cif_id: str,
        data_update_customer: dict,
        session: Session
):
    session.execute(
        update(
            Customer
        ).filter(Customer.id == cif_id).values(data_update_customer)
    )

    return ReposReturn(data=cif_id)


async def repos_get_casa_account_by_account_number(
        account_number: str,
        session: Session
):
    casa_account = session.execute(
        select(
            CasaAccount.id
        ).filter(CasaAccount.casa_account_number == account_number)
    ).scalar()

    return ReposReturn(data=casa_account)


async def repos_get_customer_open_cif(
        cif_id: str,
        session: Session
):
    customer = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress,
            CustomerProfessional,
            CustomerEmployee,
            AddressWard,
            AddressDistrict,
            AddressProvince,
            AddressCountry,
            AverageIncomeAmount
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id)
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id)
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id)
        .join(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id)
        .outerjoin(CustomerProfessional, Customer.customer_professional_id == CustomerProfessional.id)
        .outerjoin(CustomerEmployee, Customer.id == CustomerEmployee.customer_id)
        .outerjoin(AverageIncomeAmount, CustomerProfessional.average_income_amount_id == AverageIncomeAmount.id)
        .filter(Customer.id == cif_id)
    ).all()

    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="CUSTOMER_OPEN_CIF")

    return ReposReturn(data=customer)


async def repos_get_teller_info(booking_id: str, session: Session):
    transaction_daily = aliased(TransactionDaily, name="TransactionDailyRoot")

    teller = session.execute(
        select(
            TransactionSender,
            TransactionDaily,
            transaction_daily
        )
        .join(Booking, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(transaction_daily, TransactionDaily.transaction_root_id == transaction_daily.transaction_id)
        .join(TransactionSender, transaction_daily.transaction_id == TransactionSender.transaction_id)
        .filter(Booking.id == booking_id)
    ).scalar()

    return ReposReturn(data=teller)


async def repos_get_customer_avatar_url_from_cif(cif_number: str, session: Session):
    avatar_url = session.execute(
        select(
            CustomerIdentityImage.image_url
        )
        .join(CustomerIdentity, CustomerIdentityImage.identity_id == CustomerIdentity.id)
        .join(Customer, CustomerIdentity.customer_id == Customer.id)
        .filter(
            Customer.cif_number == cif_number,
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_FACE
        )
    ).scalar()

    return ReposReturn(data=avatar_url)


async def repos_check_mobile_num(mobile_num, session: Session):
    mobile_num_info = session.execute(
        select(
            Customer.mobile_number
        ).filter(Customer.mobile_number == mobile_num)
    ).scalar()

    return ReposReturn(data=mobile_num_info)


async def repos_get_transaction_jobs(
        booking_id: str,
        session: Session
):
    transaction_jobs = session.execute(
        select(
            TransactionJob
        )
        .filter(TransactionJob.booking_id == booking_id)
        .order_by(TransactionJob.business_job_id, desc(TransactionJob.created_at))
    ).scalars().all()
    return ReposReturn(data=transaction_jobs)


async def repos_gw_cif_open_casa_account(
        cif_number: str,
        self_selected_account_flag: str,
        casa_account_info: str,
        current_user,
        booking_id: str,
        session: Session
):
    """
    Repo dùng cho mở TKTT cùng lúc với mở CIF
    """
    is_success, gw_open_casa_account_info, _ = await service_gw.get_open_casa_account(
        cif_number=cif_number,
        self_selected_account_flag=self_selected_account_flag,
        casa_account_info=casa_account_info,
        current_user=current_user
    )
    error_code = None
    error_desc = None
    if not is_success:
        error_code = ERROR_CALL_SERVICE_GW
        error_desc = gw_open_casa_account_info

    session.add(TransactionJob(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_CASA_INFO,
        complete_flag=is_success,
        error_code=error_code,
        error_desc=orjson_dumps(error_desc),
        created_at=now()
    ))
    session.commit()
    return ReposReturn(data=(is_success, gw_open_casa_account_info))


@auto_commit
async def repos_update_casa_account(
        casa_account: CasaAccount,
        account_number: str,
        session: Session
):
    session.execute(
        update(
            CasaAccount
        )
        .filter(CasaAccount.id == casa_account.id)
        .values(
            casa_account_number=account_number
        )
    )
    return ReposReturn(data=None)


@auto_commit
async def repos_update_approval_status_for_ebank(
        ebank_id: str,
        session: Session
):
    session.execute(
        update(
            EBankingInfo
        )
        .filter(EBankingInfo.id == ebank_id)
        .values(
            approval_status=True
        )
    )
    return ReposReturn(data=None)


@auto_commit
async def repos_update_approval_status_for_reg_balance(
        reg_balance_id: str,
        session: Session
):
    session.execute(
        update(
            EBankingRegisterBalance
        )
        .filter(EBankingRegisterBalance.id == reg_balance_id)
        .values(
            approval_status=True
        )
    )
    return ReposReturn(data=None)


@auto_commit
async def repos_update_approval_status_for_debit_card(
        debit_card_id: str,
        session: Session
):
    session.execute(
        update(
            DebitCard
        )
        .filter(DebitCard.id == debit_card_id)
        .values(
            approval_status=True
        )
    )
    return ReposReturn(data=None)


async def repos_get_progress(booking_id: str, session: Session):
    transaction_jobs = session.execute(
        select(
            TransactionJob
        )
        .filter(TransactionJob.booking_id == booking_id)
        .order_by(TransactionJob.business_job_id, desc(TransactionJob.created_at))
    ).scalars().all()

    completed_bussiness_jobs = [
        transaction_job.business_job_id for transaction_job in transaction_jobs if transaction_job.complete_flag]

    is_complete_cif = True if BUSINESS_JOB_CODE_CIF_INFO in completed_bussiness_jobs else False
    is_complete_casa = True if BUSINESS_JOB_CODE_CASA_INFO in completed_bussiness_jobs else False
    is_complete_eb = True if BUSINESS_JOB_CODE_E_BANKING in completed_bussiness_jobs else False
    is_complete_debit = True if BUSINESS_JOB_CODE_DEBIT_CARD in completed_bussiness_jobs else False

    response = (is_complete_cif, is_complete_casa, is_complete_eb, is_complete_debit)
    return ReposReturn(data=response)


async def repos_push_cif_to_gw(booking_id: str, session: Session, response_customers: dict, current_user: any,
                               cif_id: str, maker_staff_name):
    # TODO get gdv
    # teller = self.call_repos(await repos_get_teller_info(booking_id=BOOKING_ID, session=self.oracle_session))  # noqa

    account_info = {
        "account_class_code": GW_DEFAULT_VALUE,
        "account_auto_create_cif": GW_DEFAULT_VALUE,
        "account_currency": GW_DEFAULT_VALUE,
        "acc_auto": GW_DEFAULT_VALUE,
        "account_num": GW_DEFAULT_VALUE
    }

    first_row = response_customers[0]
    customer = first_row.Customer

    cust_identity = first_row.CustomerIdentity
    cust_individual = first_row.CustomerIndividualInfo
    cust_professional = first_row.CustomerProfessional

    cif_info = {
        "cif_auto": GW_SELECT if customer.self_selected_cif_flag else GW_AUTO,
        "cif_num": customer.cif_number if customer.self_selected_cif_flag else GW_DEFAULT_VALUE
    }

    # địa chỉ thường trú
    address_info_i = {
        "line": GW_DEFAULT_VALUE,
        "ward_name": GW_DEFAULT_VALUE,
        "district_name": GW_DEFAULT_VALUE,
        "city_name": GW_DEFAULT_VALUE,
        "country_name": GW_DEFAULT_VALUE,
        "same_addr": GW_DEFAULT_VALUE
    }
    address_contact_info_i = {
        "contact_address_line": GW_DEFAULT_VALUE,
        "contact_address_ward_name": GW_DEFAULT_VALUE,
        "contact_address_district_name": GW_DEFAULT_VALUE,
        "contact_address_city_name": GW_DEFAULT_VALUE,
        "contact_address_country_name": GW_DEFAULT_VALUE
    }
    # địa chỉ đăng ký doanh nghiệp
    address_info_c = {
        "line": GW_DEFAULT_VALUE,
        "ward_name": GW_DEFAULT_VALUE,
        "district_name": GW_DEFAULT_VALUE,
        "city_name": GW_DEFAULT_VALUE,
        "country_name": GW_DEFAULT_VALUE,
        "cor_same_addr": GW_DEFAULT_VALUE
    }
    # địa chỉ liên lạc doanh nghiệp
    address_contact_info_c = {
        "contact_address_line": GW_DEFAULT_VALUE,
        "contact_address_ward_name": GW_DEFAULT_VALUE,
        "contact_address_district_name": GW_DEFAULT_VALUE,
        "contact_address_city_name": GW_DEFAULT_VALUE,
        "contact_address_country_name": GW_DEFAULT_VALUE
    }
    for row in response_customers:
        if row.CustomerAddress.address_type_id == RESIDENT_ADDRESS_CODE:
            address_info_i = {
                "line": row.CustomerAddress.address,
                "ward_name": row.AddressWard.name,
                "district_name": row.AddressDistrict.name,
                "city_name": row.AddressProvince.name,
                "country_name": row.AddressCountry.id,
                "same_addr": "Y"
            }
        else:
            address_contact_info_i = {
                "contact_address_line": row.CustomerAddress.address,
                "contact_address_ward_name": row.AddressWard.name,
                "contact_address_district_name": row.AddressDistrict.name,
                "contact_address_city_name": row.AddressProvince.name,
                "contact_address_country_name": row.AddressCountry.id
            }
    # quảng cáo từ scb
    marketing_flag = GW_YES if customer.advertising_marketing_flag else GW_NO_MARKETING_FLAG
    # thỏa thuận pháo lý
    agreement_flag = GW_YES_AGREEMENT_FLAG if customer.legal_agreement_flag else GW_NO_AGREEMENT_FLAG

    if not first_row.AverageIncomeAmount:
        return ReposReturn(
            is_error=True,
            loc="Contact Info",
            msg=ERROR_NO_DATA
        )

    # TODO hard core CN_00_CUNG_CAP_TT_FATCA, KHTC_DOI_TUONG, CUNG_CAP_DOANH_THU_THUAN
    udf_value = f"KHONG~{first_row.AverageIncomeAmount.id}~{cust_professional.career_id}~{marketing_flag}~KHONG~{agreement_flag}~{GW_DEFAULT_KHTC_DOI_TUONG}"

    issued_date = cust_identity.issued_date
    # replace issued_date_year -> 2018
    issued_date_new = issued_date.replace(year=2018)

    customer_info = {
        # TODO hard core customer category
        "customer_category": GW_DEFAULT_CUSTOMER_CATEGORY,
        "customer_type": GW_CUSTOMER_TYPE_B if customer.customer_type_id == CUSTOMER_TYPE_ORGANIZE else GW_CUSTOMER_TYPE_I,
        "cus_ekyc": customer.kyc_level_id,
        "full_name": customer.full_name_vn,
        "gender": cust_individual.gender_id,
        "telephone": customer.telephone_number if customer.telephone_number else GW_DEFAULT_VALUE,
        "mobile_phone": customer.mobile_number if customer.mobile_number else GW_DEFAULT_VALUE,
        "email": customer.email if customer.email else GW_DEFAULT_VALUE,
        "place_of_birth": cust_individual.country_of_birth_id if cust_individual.country_of_birth_id else GW_DEFAULT_VALUE,
        "birthday": date_to_string(cust_individual.date_of_birth,
                                   _format=GW_DATE_FORMAT) if cust_individual.date_of_birth else GW_DEFAULT_VALUE,
        "tax": customer.tax_number if customer.tax_number else GW_DEFAULT_VALUE,
        # TODO hard core tình trạng cư trú (resident_status)
        "resident_status": "N",
        "legal_guardian": GW_DEFAULT_VALUE,
        "co_owner": GW_DEFAULT_VALUE,
        "nationality": customer.nationality_id if customer.nationality_id else GW_DEFAULT_VALUE,
        "birth_country": GW_DEFAULT_VALUE,
        # TODO hard core language
        "language": GW_LANGUAGE,
        "local_code": GW_LOCAL_CODE,
        "current_official": GW_DEFAULT_VALUE,
        "biz_license_issue_date": GW_DEFAULT_VALUE,
        "cor_capital": GW_DEFAULT_VALUE,
        "cor_email": GW_DEFAULT_VALUE,
        "cor_fax": GW_DEFAULT_VALUE,
        "cor_tel": GW_DEFAULT_VALUE,
        "cor_mobile": GW_DEFAULT_VALUE,
        "cor_country": GW_DEFAULT_VALUE,
        "cor_desc": GW_DEFAULT_VALUE,
        "coowner_relationship": GW_DEFAULT_VALUE,
        "martial_status": cust_individual.marital_status_id,
        "p_us_res_status": "N",
        "p_vst_us_prev": "N",
        "p_field9": GW_DEFAULT_VALUE,
        "p_field10": GW_DEFAULT_VALUE,
        "p_field11": GW_DEFAULT_VALUE,
        "p_field12": GW_DEFAULT_VALUE,
        "p_field13": GW_DEFAULT_VALUE,
        "p_field14": GW_DEFAULT_VALUE,
        "p_field15": GW_DEFAULT_VALUE,
        "p_field16": GW_DEFAULT_VALUE,
        "cif_info": cif_info,
        "id_info_main": {
            "id_num": cust_identity.identity_num,
            "id_issued_date": date_to_string(issued_date_new, _format=GW_DATE_FORMAT),
            "id_expired_date": date_to_string(cust_identity.expired_date, _format=GW_DATE_FORMAT),
            "id_issued_location": cust_identity.place_of_issue_id,
            "id_type": GW_DEFAULT_TYPE_ID
        },
        "address_info_i": address_info_i,
        "address_contact_info_i": address_contact_info_i,
        "address_info_c": address_info_c,
        "address_contact_info_c": address_contact_info_c,
        "id_info_extra": {
            "id_num": GW_DEFAULT_VALUE,
            "id_issued_date": GW_DEFAULT_VALUE,
            "id_expired_date": GW_DEFAULT_VALUE,
            "id_issued_location": GW_DEFAULT_VALUE,
            "id_type": GW_DEFAULT_VALUE
        },
        "branch_info": {
            "branch_code": current_user.user_info.hrm_branch_code
        },
        "job_info": {
            # TODO chưa đồng bộ data giữa core và crm
            "professional_code": "T_0806",
            "position": cust_professional.position_id if cust_professional.position_id else GW_DEFAULT_VALUE,
            "official_telephone": cust_professional.company_phone if cust_professional.company_phone else GW_DEFAULT_VALUE,
            "address_office_info": {
                "address_full": cust_professional.company_address if cust_professional.company_address else GW_DEFAULT_VALUE
            }
        },
        "staff_info_checker": {
            "staff_name": current_user.user_info.username
        },
        "staff_info_maker": {
            "staff_name": maker_staff_name
        },
        "udf_info": {
            "udf_name": GW_UDF_NAME,
            "udf_value": udf_value
        }
    }

    data_input = {
        "customer_info": customer_info,
        "account_info": account_info
    }

    is_success, response_data = await service_gw.open_cif(
        data_input=data_input,
        current_user=current_user.user_info
    )

    await repos_save_transaction_jobs(
        session=session,
        booking_id=booking_id,
        is_success=is_success,
        response_data=response_data,
        business_job_ids=[BUSINESS_JOB_CODE_INIT, BUSINESS_JOB_CODE_CIF_INFO]
    )

    # check open_cif success
    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="repos_push_cif_to_gw -> service_gw.open_cif",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(response_data)
        )

    cif_number = response_data['openCIFAuthorise_out']['data_output']['customner_info']['cif_info']['cif_num']

    # call repos update cif_number and account_number
    await repos_update_cif_number_customer(
        cif_id=cif_id,
        data_update_customer={
            "cif_number": cif_number,
            "complete_flag": CUSTOMER_COMPLETED_FLAG
        },
        session=session
    )

    session.commit()

    return ReposReturn(data=cif_number)


async def repos_push_casa_to_gw(booking_id: str, session: Session, current_user: any,
                                cif_id: str, cif_number: str, maker_staff_name, casa_account_ids: List[str] = None):

    is_success = False

    # MỞ CASA: không có cif_id
    if not cif_id:
        payment_account_list_result = await repos_get_detail_payment_accounts_by_account_ids(
            casa_account_ids=casa_account_ids,
            session=session
        )
        if payment_account_list_result.is_error:
            return ReposReturn(
                is_error=True,
                msg=payment_account_list_result.msg,
                loc=payment_account_list_result.loc,
                detail=payment_account_list_result.detail,
                error_status_code=payment_account_list_result.error_status_code
            )

        for payment_account in payment_account_list_result.data:

            casa_account = payment_account[0]

            is_success, gw_open_casa_account_info, _ = await service_gw.get_open_casa_account(
                cif_number=cif_number,
                self_selected_account_flag=casa_account.self_selected_account_flag,
                casa_account_info=casa_account,
                current_user=current_user.user_info,
                maker_staff_name=maker_staff_name
            )

            if not is_success:
                return ReposReturn(
                    is_error=True,
                    loc="open_casa",
                    msg=ERROR_CALL_SERVICE_GW,
                    detail=str(gw_open_casa_account_info)
                )

            account_number = gw_open_casa_account_info['openCASA_out']['data_output']['account_info']['account_num']

            # cập nhật lại casa_number
            await repos_update_casa_account(
                casa_account=casa_account, account_number=account_number, session=session
            )

    # MỞ CIF: có cif_id
    else:
        detail_payment_account_info_result = await repos_get_detail_payment_account(
            cif_id=cif_id,
            session=session
        )
        if detail_payment_account_info_result.is_error:
            return ReposReturn(
                is_error=True,
                msg=detail_payment_account_info_result.msg,
                loc=detail_payment_account_info_result.loc,
                detail=detail_payment_account_info_result.detail,
                error_status_code=detail_payment_account_info_result.error_status_code
            )

        (
            casa_account, currency, account_class, account_type, account_structure_type,
            account_structure_type_level_2, account_structure_type_level_1, address_country
        ) = detail_payment_account_info_result.data

        is_success, gw_open_casa_account_info, _ = await service_gw.get_open_casa_account(
            cif_number=cif_number,
            self_selected_account_flag=casa_account.self_selected_account_flag,
            casa_account_info=casa_account,
            current_user=current_user.user_info,
            maker_staff_name=maker_staff_name
        )

        if not is_success:
            return ReposReturn(
                is_error=True,
                loc="open_casa",
                msg=ERROR_CALL_SERVICE_GW,
                detail=str(gw_open_casa_account_info)
            )

        account_number = gw_open_casa_account_info['openCASA_out']['data_output']['account_info']['account_num']

        # cập nhật lại casa_number
        await repos_update_casa_account(
            casa_account=casa_account, account_number=account_number, session=session
        )

    # error_code = ""
    # error_desc = ""
    # if not is_success:
    #     error_code = ERROR_CALL_SERVICE_GW
    #     error_desc = orjson_dumps(gw_open_casa_account_info) if gw_open_casa_account_info else ""
    #
    # session.add(TransactionJob(
    #     transaction_id=generate_uuid(),
    #     booking_id=booking_id,
    #     business_job_id=BUSINESS_JOB_CODE_CASA_INFO,
    #     complete_flag=is_success,
    #     error_code=error_code,
    #     error_desc=error_desc,
    #     created_at=now()
    # ))
    #
    # session.commit()

    return ReposReturn(data=None)

    # return ReposReturn(data=account_number)


async def repos_push_internet_banking_to_gw(booking_id: str,
                                            session: Session,
                                            response_customers: dict,
                                            current_user: any,
                                            cif_id: str,
                                            cif_number: str,
                                            casa_account_number: str,
                                            maker_staff_name: str):
    first_row = response_customers[0]
    customer = first_row.Customer
    cust_individual = first_row.CustomerIndividualInfo

    # Lấy thông tin EB từ DB
    e_banking_result = await repos_get_e_banking_from_db_by_cif_id(
        cif_id=cif_id, session=session)
    if e_banking_result.is_error:
        return ReposReturn(
            is_error=True,
            msg=e_banking_result.msg,
            loc=e_banking_result.loc,
            detail=e_banking_result.detail,
            error_status_code=e_banking_result.error_status_code
        )
    e_banking = e_banking_result.data

    # Lấy thông tin SMS casa từ DB
    balance_id__relationship_mobile_numbers_result = await repos_get_sms_casa_mobile_number_from_db_by_cif_id(
        cif_id=cif_id, session=session)

    if balance_id__relationship_mobile_numbers_result.is_error:
        return ReposReturn(
            is_error=True,
            msg=balance_id__relationship_mobile_numbers_result.msg,
            loc=balance_id__relationship_mobile_numbers_result.loc,
            detail=balance_id__relationship_mobile_numbers_result.detail,
            error_status_code=balance_id__relationship_mobile_numbers_result.error_status_code
        )

    balance_id__relationship_mobile_numbers = balance_id__relationship_mobile_numbers_result.data

    # Không tìm thấy thông tin từ DB có thể do khách hàng không đăng ký, hoặc đã đăng ký thành công từ lần trước
    if not e_banking and not balance_id__relationship_mobile_numbers:
        return ReposReturn(data=None)

    # Push GW EBANK
    error_messages = []
    is_success_eb = False
    is_success_sms = False

    if e_banking:
        authentication_info = []
        for authentication_code in e_banking["authentication_info_list"]:
            authentication_info.append({
                "authentication_code": authentication_code
            })

        e_banking_info = {
            "ebank_ibmb_info": {
                "ebank_ibmb_username": e_banking["account_name"],
                "ebank_ibmb_mobilephone": customer.mobile_number
            },
            "cif_info": {
                "cif_num": cif_number
            },
            "address_info": {
                "line": first_row.CustomerAddress.address,
                "ward_name": first_row.AddressWard.name,
                "district_name": first_row.AddressDistrict.name,
                "city_name": first_row.AddressProvince.name,
                "city_code": first_row.AddressCountry.id
            },
            "customer_info": {
                "full_name": customer.full_name_vn,
                "first_name": split_name(customer.full_name_vn)[2] if split_name(customer.full_name_vn)[2] else " ",
                "middle_name": split_name(customer.full_name_vn)[1] if split_name(customer.full_name_vn)[1] else " ",
                "last_name": split_name(customer.full_name_vn)[0],
                "birthday": date_to_string(cust_individual.date_of_birth,
                                           _format=GW_DATE_FORMAT) if cust_individual.date_of_birth else GW_DEFAULT_VALUE,
                "email": customer.email if customer.email else GW_DEFAULT_VALUE
            },
            "authentication_info": authentication_info,
            "service_package_info": {
                "service_package_code": GW_DEFAULT_VALUE
            },
            "staff_referer": {
                "staff_code": GW_DEFAULT_VALUE
            }
        }

        is_success_eb, eb_response_data = await service_gw.get_open_ib(
            current_user=current_user.user_info,
            data_input=e_banking_info
        )

        if is_success_eb:
            await repos_update_approval_status_for_ebank(
                ebank_id=e_banking['id'], session=session
            )
        else:
            error_messages.append(eb_response_data)

    # Push GW SMS
    if balance_id__relationship_mobile_numbers:
        ebank_sms_info_list = []
        reg_balance_id = None
        for balance_id, mobile_numbers in balance_id__relationship_mobile_numbers.items():
            ebank_sms_info_list = [{
                "ebank_sms_info_item": {
                    "ebank_sms_indentify_num": mobile_number,
                    "cif_info": {
                        "cif_num": cif_number
                    },
                    "branch_info": {
                        "branch_code": current_user.user_info.hrm_branch_code
                    }
                }
            } for mobile_number in mobile_numbers]

            reg_balance_id = balance_id

        # @TODO: hard code account_type là "TT" biến động số dư
        account_info = {
            "account_num": casa_account_number,
            "account_type": "TT"
        }
        staff_info_checker = {
            "staff_name": current_user.user_info.username
        }
        staff_info_maker = {
            "staff_name": maker_staff_name
        }

        is_success_sms, sms_response_data = await service_gw.register_sms_service_by_account_casa(
            current_user=current_user.user_info,
            account_info=account_info,
            ebank_sms_info_list=ebank_sms_info_list,
            staff_info_checker=staff_info_checker,
            staff_info_maker=staff_info_maker
        )

        if is_success_sms:
            await repos_update_approval_status_for_reg_balance(
                reg_balance_id=reg_balance_id, session=session
            )
        else:
            error_messages.append(sms_response_data)

    # Lưu transaction job
    await repos_save_transaction_jobs(
        session=session,
        booking_id=booking_id,
        is_success=False if error_messages else True,
        response_data=error_messages,
        business_job_ids=[BUSINESS_JOB_CODE_E_BANKING]
    )

    if error_messages:
        return ReposReturn(
            is_error=True,
            loc="open_cif -> repos_push_internet_banking_to_gw",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(error_messages)
        )

    return ReposReturn(data=None)


async def repos_push_debit_to_gw(booking_id: str, session: Session, current_user, cif_id: str, cif_number: str,
                                 casa_account_number, response_customers, maker_staff_name):
    card_result = await repos_debit_card(
        cif_id=cif_id, session=session)
    if card_result.is_error:
        return ReposReturn(
            is_error=True,
            msg=card_result.msg,
            loc=card_result.loc,
            detail=card_result.detail,
            error_status_code=card_result.error_status_code
        )

    card_data = card_result.data
    debit_card_id = card_data['debit_card_id']
    customer_info = response_customers[0]

    # @TODO: card_auto_renew, Quan hệ với thẻ chính, Tên mẹ của khách hàng
    # @TODO: Câu hỏi bí mật, Nơi nhân hóa đơn, Nơi nhân sao kê
    card_info = {
        "card_indicator": MAIN_CARD,
        "card_type": card_data["issue_debit_card"]["card_group"],
        "card_auto_renew": GW_DEFAULT_CARD_AUTO_RENEW,
        "card_release_form": GW_DEFAULT_NORMAL if card_data["issue_debit_card"]["physical_issuance_type"]["code"] else GW_DEFAULT_QUICK,
        "card_block_online_trans": GW_DEFAULT_YES if card_data["issue_debit_card"]["payment_online_flag"] else GW_DEFAULT_NO,
        "card_contact_less": GW_DEFAULT_YES if card_data["issue_debit_card"]["physical_card_type"][0]["code"] == 1 else GW_DEFAULT_NO,
        "card_relation_to_primany": GW_DEFAULT_CARD_RELATION_TO_PRIMARY,
        "card_mother_name": customer_info.Customer.full_name_vn,
        "card_secure_question": customer_info.Customer.full_name_vn,
        "card_bill_option": GW_DEFAULT_CARD_BILL_OPTION,
        "card_statement_delivery_option": GW_DEFAULT_CARD_STATEMENT_DELIVERY_OPTION,
        "card_customer_type": card_data["issue_debit_card"]["customer_type"]["id"],
        "srcCde": card_data["issue_debit_card"]["src_code"],
        "promoCde": card_data["issue_debit_card"]["pro_code"],

        # additional field
        "account_type": GW_DEFAULT_ATM_CARD_ACCOUNT_PROVIDER,
        "title": GW_CUST_TITLE_MR if customer_info.CustomerIndividualInfo.title_id == CRM_CUST_TITLE_MR else GW_CUST_TITLE_MRS,
        "full_name_vn": f'{card_data["information_debit_card"]["name_on_card"]["last_name_on_card"]} '
                        f'{card_data["information_debit_card"]["name_on_card"]["middle_name_on_card"]} '
                        f'{card_data["information_debit_card"]["name_on_card"]["first_name_on_card"]}',
        "last_name": card_data["information_debit_card"]["name_on_card"]["last_name_on_card"],
        "first_name": card_data["information_debit_card"]["name_on_card"]["first_name_on_card"],
        "middle_name": card_data["information_debit_card"]["name_on_card"]["middle_name_on_card"],

        # địa chỉ nhận thẻ
        "delivByBrchInd": GW_DEFAULT_YES
        if card_data["card_delivery_address"]["delivery_address_flag"] == CRM_DELIVERY_ADDRESS_FLAG_FALSE else GW_DEFAULT_NO,
        "address_info_line": card_data["card_delivery_address"]["delivery_address"]["number_and_street"],
        "address_info_ward_name": card_data["card_delivery_address"]["delivery_address"]["ward"],
        "address_info_district_name": card_data["card_delivery_address"]["delivery_address"]["district"],
        "address_info_city_name": card_data["card_delivery_address"]["delivery_address"]["province"],

        # thông tin chi nhánh nhận thẻ
        "delivBrchId": card_data["card_delivery_address"]["scb_branch"]["id"]
    }

    # Thông tin nhân viên giới thiệu
    direct_staff = ""
    indirect_staff = ""
    for row in response_customers:
        if row.CustomerEmployee:
            if row.CustomerEmployee.staff_type_id == STAFF_TYPE_BUSINESS_CODE:
                direct_staff = row.CustomerEmployee.employee_id
            else:
                indirect_staff = row.CustomerEmployee.employee_id

    if not direct_staff or not indirect_staff:
        return ReposReturn(
            is_error=True,
            msg=ERROR_NO_DATA,
            loc="open_cif -> repos_push_debit_to_gw",
            detail="direct_staff and indirect_staff cannot null"
        )

    # Loại tiền tệ của TKTT
    casa_currency_number = await repos_get_casa_account_currency_number(session=session, cif_id=cif_id)

    is_success, response_data = await service_gw.open_cards(
        current_user=current_user.user_info,
        cif_number=cif_number,
        casa_account_number=casa_account_number,
        card_info=card_info,
        customer_info=response_customers[0],
        maker_staff_name=maker_staff_name,
        direct_staff=direct_staff,
        indirect_staff=indirect_staff,
        casa_currency_number=casa_currency_number.data
    )

    await repos_save_transaction_jobs(
        session=session,
        booking_id=booking_id,
        is_success=is_success,
        response_data=response_data,
        business_job_ids=[BUSINESS_JOB_CODE_DEBIT_CARD]
    )

    if not is_success:
        return ReposReturn(
            is_error=True,
            loc="open_cif -> repos_push_debit_to_gw",
            msg=ERROR_CALL_SERVICE_GW,
            detail=str(response_data)
        )

    # cập nhật lại approval_status cho card
    await repos_update_approval_status_for_debit_card(
        debit_card_id=debit_card_id, session=session
    )

    return ReposReturn(data=None)


async def repos_get_cif_number_open_cif(cif_id: str, session: Session):
    cif_number = session.execute(
        select(
            Customer.cif_number
        ).filter(
            Customer.id == cif_id
        )
    ).scalars().first()

    if not cif_number:
        return ReposReturn(
            is_error=True,
            loc="repos_get_cif_number_open_cif",
            msg=ERROR_NO_DATA
        )

    return ReposReturn(data=cif_number)


async def repos_get_casa_account_number_open_cif(cif_id: str, session: Session):
    casa_account_number = session.execute(
        select(
            CasaAccount.casa_account_number
        ).filter(
            CasaAccount.customer_id == cif_id
        )
    ).scalars().first()

    if not casa_account_number:
        return ReposReturn(
            is_error=True,
            loc="open_cif -> repos_push_debit_to_gw -> casa_account_number",
            msg=ERROR_NO_DATA
        )

    return ReposReturn(data=casa_account_number)


async def repos_get_casa_account_currency_number(session: Session, cif_id: str):

    currency_info = session.execute(
        select(
            CasaAccount,
            Currency.number
        )
        .outerjoin(Currency, CasaAccount.currency_id == Currency.id)
        .filter(CasaAccount.customer_id == cif_id)
    ).first()

    if not currency_info:
        return ReposReturn(
            is_error=True,
            loc="open_cif -> push e-bank and sms casa to gw -> repos_get_casa_account_currency_number",
            msg=ERROR_NO_DATA
        )

    return ReposReturn(data=currency_info.number)


@auto_commit
async def repos_save_transaction_jobs(
    session: Session,
    booking_id: str,
    is_success: bool,
    response_data: list,
    business_job_ids: List[str]
):
    for business_job_id in business_job_ids:
        session.add(TransactionJob(**{
            "transaction_id": generate_uuid(),
            "booking_id": booking_id,
            "business_job_id": business_job_id,
            "complete_flag": is_success,
            "error_code": "" if is_success else ERROR_CALL_SERVICE_GW,
            "error_desc": "" if is_success else orjson_dumps(response_data),
            "created_at": now(),
            "updated_at": now()
        }))

    return ReposReturn(data=None)
