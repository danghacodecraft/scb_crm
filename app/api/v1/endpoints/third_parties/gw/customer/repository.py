from typing import List

from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn, auto_commit
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
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, TransactionJob
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_CASA_INFO
from app.utils.constant.cif import BUSINESS_FORM_OPEN_CIF_PD, IMAGE_TYPE_FACE
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_NO_DATA, ERROR_OPEN_CIF
)
from app.utils.functions import generate_uuid, now, orjson_dumps


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
        # data_update_casa_account: dict,
        session: Session
):
    session.execute(
        update(
            Customer
        ).filter(Customer.id == cif_id).values(data_update_customer)
    )

    # if data_update_casa_account:
    #     session.execute(
    #         update(
    #             CasaAccount
    #         ).filter(CasaAccount.customer_id == cif_id).values(data_update_casa_account)
    #     )

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
    is_success, gw_open_casa_account_info, form_data = await service_gw.get_open_casa_account(
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

    session.add(TransactionJob(**dict(
        transaction_id=generate_uuid(),
        booking_id=booking_id,
        business_job_id=BUSINESS_JOB_CODE_CASA_INFO,
        complete_flag=is_success,
        error_code=error_code,
        error_desc=error_desc,
        created_at=now()
    )))
    session.commit()
    return ReposReturn()
