import random
import re
from typing import List

from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress, CustomerProfessional
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.e_banking.model import TdAccount
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer
)
from app.third_parties.oracle.models.cif.other_information.model import (
    CustomerEmployee
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerCategory, CustomerClassification, CustomerEconomicProfession,
    CustomerGender, CustomerStatus, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, Career, KYCLevel, MaritalStatus, Position,
    ResidentStatus
)
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.constant.cif import (
    STAFF_TYPE_BUSINESS_CODE, STAFF_TYPE_REFER_INDIRECT_CODE
)
from app.utils.error_messages import (
    ERROR_BOOKING_CODE_NOT_EXIST, ERROR_CIF_ID_NOT_EXIST,
    ERROR_CIF_NUMBER_EXIST, ERROR_CIF_NUMBER_INVALID,
    ERROR_CIF_NUMBER_NOT_EXIST, MESSAGE_STATUS
)
from app.utils.functions import dropdown, now


async def repos_get_initializing_customer(cif_id: str, session: Session) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(
            Customer.id == cif_id,
            Customer.complete_flag == 0
        )
    ).scalar()
    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=customer)


async def repos_get_customer(cif_id: str, session: Session) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(
            Customer.id == cif_id
        )
    ).scalar()
    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=customer)


async def repos_get_cif_info(cif_id: str, session: Session) -> ReposReturn:
    customer_info = session.execute(
        select(
            Customer.cif_number,
            Customer.self_selected_cif_flag,
            CustomerClassification,
            CustomerEconomicProfession,
            KYCLevel
        )
        .join(CustomerClassification, Customer.customer_classification_id == CustomerClassification.id)
        .join(CustomerEconomicProfession, Customer.customer_economic_profession_id == CustomerEconomicProfession.id)
        .join(KYCLevel, Customer.kyc_level_id == KYCLevel.id)
        .filter(
            Customer.id == cif_id,
            Customer.active_flag == 1
        )
    ).first()
    if not customer_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_ID_NOT_EXIST,
            loc='cif_id'
        )
    cif_number, self_selected_cif_flag, customer_classification, customer_economic_profession, kyc_level = customer_info
    return ReposReturn(data={
        "self_selected_cif_flag": self_selected_cif_flag,
        "cif_number": cif_number,
        "customer_classification": dropdown(customer_classification),
        "customer_economic_profession": dropdown(customer_economic_profession),
        "kyc_level": dropdown(kyc_level)
    })


async def repos_profile_history(cif_id: str, session: Session) -> ReposReturn:
    histories = session.execute(
        select(
            BookingCustomer,
            Booking,
            BookingBusinessForm
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id)
        .filter(
            BookingCustomer.customer_id == cif_id
        )
    ).all()

    # if not histories:
    #     return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=histories)


async def repos_customer_information(cif_id: str, session: Session) -> ReposReturn:
    query_data_customer = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            ResidentStatus,
            CustomerAddress,
            CustomerStatus,
            PlaceOfIssue,
            AddressCountry,
            CustomerClassification,
            CustomerGender,
            MaritalStatus,
            CustomerType,
            CustomerCategory
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .outerjoin(ResidentStatus, CustomerIndividualInfo.resident_status_id == ResidentStatus.id)
        .join(CustomerStatus, Customer.customer_status_id == CustomerStatus.id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id)
        .join(CustomerClassification, Customer.customer_classification_id == CustomerClassification.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .outerjoin(MaritalStatus, CustomerIndividualInfo.marital_status_id == MaritalStatus.id)
        .outerjoin(CustomerType, Customer.customer_type_id == CustomerType.id)
        .outerjoin(CustomerCategory, Customer.customer_category_id == CustomerCategory.id)
        .filter(
            Customer.id == cif_id
        ).order_by(desc(CustomerIdentity.maker_at))
    ).all()

    if not query_data_customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=query_data_customer)


async def repos_get_customer_identity(cif_id: str, session: Session):
    identity = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not identity:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    return ReposReturn(data=identity)


async def repos_check_not_exist_cif_number(cif_number: str, session: Session) -> ReposReturn:
    # TODO: call to core
    cif_number = session.execute(
        select(
            Customer.cif_number
        ).filter(Customer.cif_number == cif_number)
    ).scalars().first()

    if cif_number:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc="cif_number")

    return ReposReturn(data='Cif number is not exist')


async def repos_get_customers_by_cif_numbers(
        cif_numbers: List[str],
        session: Session
) -> ReposReturn:
    customers = session.execute(
        select(
            Customer
        ).filter(
            Customer.cif_number.in_(cif_numbers),
            Customer.complete_flag == 1
        )
    ).scalars().all()
    if not customers or len(cif_numbers) != len(customers):
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number"
        )

    return ReposReturn(data=customers)


async def repos_validate_cif_number(cif_number: str):
    regex = re.search("[0-9]+", cif_number)
    if not regex or len(regex.group()) != len(cif_number):
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_INVALID,
            detail=f"{MESSAGE_STATUS[ERROR_CIF_NUMBER_INVALID]}: cif_number={cif_number}",
            loc="cif_number"
        )
    return ReposReturn(data=None)


async def repos_get_total_participants(
        cif_id: str,
        session: Session
):
    total_participants = session.execute(
        select(
            BookingBusinessForm.log_data,
            BookingCustomer,
            Booking
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).scalars().all()

    return ReposReturn(data=total_participants)


async def repos_get_booking(
        cif_id: str,
        session: Session
):
    booking = session.execute(
        select(
            Booking,
            BookingCustomer
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).scalar()
    if not booking:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_CODE_NOT_EXIST)
    return ReposReturn(data=booking)


async def repos_get_booking_account(
        account_id: str,
        session: Session
):
    booking_parent_id = session.execute(
        select(
            Booking.parent_id,
            BookingAccount
        )
        .join(Booking, BookingAccount.booking_id == Booking.id)
        .filter(BookingAccount.account_id == account_id)
    ).scalar()
    if not booking_parent_id:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_CODE_NOT_EXIST)

    booking_parent = session.execute(
        select(
            Booking
        )
        .filter(Booking.id == booking_parent_id)
    ).scalar()
    if not booking_parent:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_CODE_NOT_EXIST, loc="booking_parent")

    return ReposReturn(data=booking_parent)


async def repos_get_customer_working_infos(
        cif_id_or_number: str,
        session: Session
):
    customer_working_info = session.execute(
        select(
            Customer,
            CustomerProfessional,
            Career,
            AverageIncomeAmount,
            Position
        )
        .join(CustomerProfessional, Customer.customer_professional_id == CustomerProfessional.id)
        .outerjoin(Career, CustomerProfessional.career_id == Career.id)
        .outerjoin(AverageIncomeAmount, CustomerProfessional.average_income_amount_id == AverageIncomeAmount.id)
        .outerjoin(Position, CustomerProfessional.position_id == Position.id)
        .filter(or_(Customer.id == cif_id_or_number, Customer.id == cif_id_or_number))
    ).first()

    return ReposReturn(data=customer_working_info)


async def repos_get_cif_id_by_cif_number(cif_number: str, session: Session):
    cif_id = session.execute(select(Customer.id).filter(Customer.cif_number == cif_number)).scalar()
    return ReposReturn(data=cif_id)


async def repos_get_account_id_by_account_number(account_number: str, session: Session):
    response_data = {}
    casa_accounts = session.execute(
        select(
            CasaAccount,
            Customer
        ).join(Customer, CasaAccount.customer_id == Customer.id)
        .filter(CasaAccount.casa_account_number == account_number)
    ).all()

    if casa_accounts:
        for item in casa_accounts:
            response_data.update({
                "account_id": item.CasaAccount.id,
                "customer_id": item.Customer.id
            })
        return ReposReturn(data=response_data)
    else:
        td_accounts = session.execute(
            select(
                TdAccount,
                Customer
            ).join(Customer, TdAccount.customer_id == Customer.id)
            .filter(TdAccount.td_account_number == account_number)
        ).all()

    if td_accounts:
        for item in td_accounts:
            response_data.update({
                "account_id": item.TdAccount.id,
                "customer_id": item.Customer.id
            })
        return ReposReturn(data=response_data)

    if not response_data:
        return ReposReturn(is_error=True, msg="account_number is not exist", detail=f"account_number: {account_number}")


@auto_commit
async def repos_clone_cif(cif_id: str, session: Session) -> ReposReturn:
    customer_info = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress
        )
        .join(CustomerIdentity, CustomerIdentity.customer_id == Customer.id)
        .join(CustomerIndividualInfo, CustomerIndividualInfo.customer_id == Customer.id)
        .filter(
            Customer.id == cif_id,
            Customer.active_flag == 1
        )
    ).first()
    if not customer_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_ID_NOT_EXIST,
            loc='cif_id'
        )

    customer, customer_identity, customer_individual, customer_address = customer_info

    mobile_num = ""
    for _ in range(6):
        num = str(random.randint(0, 9))
        mobile_num += num

    new_customer = Customer(**{
        'tax_number': customer.tax_number,
        'full_name': "NGUYEN VAN CHI",
        'self_selected_cif_flag': customer.self_selected_cif_flag,
        'channel_id': customer.channel_id,
        'customer_relationship_flag': customer.customer_relationship_flag,
        'full_name_vn': "NGUYỄN VĂN CHÍ",
        'legal_agreement_flag': customer.legal_agreement_flag,
        'avatar_url': customer.avatar_url,
        'customer_type_id': customer.customer_type_id,
        'first_name': "CHI",
        'advertising_marketing_flag': customer.advertising_marketing_flag,
        'complete_flag': 0,
        'cif_number': None,
        'customer_category_id': customer.customer_category_id,
        'middle_name': "VAN",
        'active_flag': customer.active_flag,
        'grade_name': customer.grade_name,
        'telephone_number': customer.telephone_number,
        'customer_economic_profession_id': customer.customer_economic_profession_id,
        'last_name': "NGUYEN",
        'open_cif_at': customer.open_cif_at,
        'mobile_number': "0969" + mobile_num,
        'customer_classification_id': customer.customer_classification_id,
        'short_name': "chinv",
        'open_branch_id': customer.open_branch_id,
        'extra_number': customer.extra_number,
        'fax_number': customer.fax_number,
        'customer_professional_id': customer.customer_professional_id,
        'email': customer.email,
        'kyc_level_id': customer.kyc_level_id,
        'cust_relationship_type_id': customer.cust_relationship_type_id,
        'customer_status_id': customer.customer_status_id,
        'nationality_id': customer.nationality_id
    })

    session.add(new_customer)
    session.flush()

    identity_num = ""
    for _ in range(len(customer_identity.identity_num)):
        num = str(random.randint(0, 9))
        identity_num += num

    new_customer_identity = CustomerIdentity(**{
        "identity_type_id": customer_identity.identity_type_id,
        "customer_id": new_customer.id,
        "identity_num": identity_num,
        "issued_date": customer_identity.issued_date,
        "expired_date": customer_identity.expired_date,
        "place_of_issue_id": customer_identity.place_of_issue_id,
        "passport_type_id": customer_identity.passport_type_id,
        "passport_code_id": customer_identity.passport_code_id,
        "primary_flag": customer_identity.primary_flag,
        "mrz_content": customer_identity.mrz_content,
        "qrcode_content": customer_identity.qrcode_content,
        "maker_at": customer_identity.maker_at,
        "maker_id": customer_identity.maker_id,
        "updater_at": customer_identity.updater_at,
        "updater_id": customer_identity.updater_id,
        "identity_number_in_passport": customer_identity.identity_number_in_passport,
        "signer": customer_identity.signer,
        "ocr_result": customer_identity.ocr_result,
    })

    session.add(new_customer_identity)

    new_customer_individual = CustomerIndividualInfo(**{
        "customer_id": new_customer.id,
        "gender_id": customer_individual.gender_id,
        "title_id": customer_individual.title_id,
        "place_of_birth_id": customer_individual.place_of_birth_id,
        "country_of_birth_id": customer_individual.country_of_birth_id,
        "resident_status_id": customer_individual.resident_status_id,
        "religion_id": customer_individual.religion_id,
        "nation_id": customer_individual.nation_id,
        "marital_status_id": customer_individual.marital_status_id,
        "date_of_birth": customer_individual.date_of_birth,
        "under_15_year_old_flag": customer_individual.under_15_year_old_flag,
        "guardian_flag": customer_individual.guardian_flag,
        "identifying_characteristics": customer_individual.identifying_characteristics,
        "father_full_name": customer_individual.father_full_name,
        "mother_full_name": customer_individual.mother_full_name,
    })

    session.add(new_customer_individual)

    new_customer_address = CustomerAddress(**{
        "customer_id": new_customer.id,
        "address_type_id": customer_address.address_type_id,
        "address_country_id": customer_address.address_country_id,
        "address_province_id": customer_address.address_province_id,
        "address_district_id": customer_address.address_district_id,
        "address_ward_id": customer_address.address_ward_id,
        "address": customer_address.address,
        "zip_code": customer_address.zip_code,
        "latitude": customer_address.latitude,
        "longitude": customer_address.longitude,
        "address_primary_flag": customer_address.address_primary_flag,
        "address_domestic_flag": customer_address.address_domestic_flag,
        "address_2": customer_address.address_2,
        "address_same_permanent_flag": customer_address.address_same_permanent_flag,
    })

    session.add(new_customer_address)

    # BOOKING
    booking = Booking(**{
        "transaction_id": "6EFE4FD4D5024A8C8E927F47C751FEEF",
        "code": "143_CRM_CIF_20220817_0000064",
        "business_type_id": BUSINESS_TYPE_INIT_CIF,
        "branch_id": "001",
        "created_at": now(),
        "updated_at": now(),
        "created_by": "DIEPTTN1"
    })

    session.add(booking)
    session.flush()

    booking_customer = BookingCustomer(**{
        "customer_id": new_customer.id,
        "booking_id": booking.id
    })
    session.add(booking_customer)
    session.flush()

    customer_employees = session.execute(
        select(
            CustomerEmployee
        )
        .filter(
            CustomerEmployee.customer_id == cif_id,
        )
    ).scalars().all()

    direct_staff = ""
    indirect_staff = ""
    for customer_employee in customer_employees:
        if customer_employee.staff_type_id == STAFF_TYPE_BUSINESS_CODE:
            direct_staff = customer_employee.employee_id
        else:
            indirect_staff = customer_employee.employee_id

    if not direct_staff or not indirect_staff:
        session.rollback()
        return ReposReturn(is_error=True, detail="Missing direct_staff, indirect_staff")

    direct_staff_customer_employee = CustomerEmployee(**{
        "staff_type_id": STAFF_TYPE_BUSINESS_CODE,
        "employee_id": direct_staff,
        "customer_id": new_customer.id,
        "created_at": now(),
        "updated_at": now()
    })
    session.add(direct_staff_customer_employee)

    indirect_staff_customer_employee = CustomerEmployee(**{
        "staff_type_id": STAFF_TYPE_REFER_INDIRECT_CODE,
        "employee_id": indirect_staff,
        "customer_id": new_customer.id,
        "created_at": now(),
        "updated_at": now()
    })
    session.add(indirect_staff_customer_employee)

    return ReposReturn(data=(new_customer.id, booking.id))
