from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.user.schema import AuthResponse
from app.settings.event import service_gw
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
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    AverageIncomeAmount, TransactionJob
)
from app.utils.error_messages import (
    ERROR_CALL_SERVICE_GW, ERROR_NO_DATA, ERROR_OPEN_CIF
)


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
    is_success, customer_info = await service_gw.get_customer_info_detail(
        customer_cif_number=cif_number, current_user=current_user.user_info
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


async def repos_gw_open_cif(
    cif_id: str,
    customer_info: dict,
    account_info: dict,
    current_user,
    transaction_job: dict,
    session: Session
):
    is_success, response_data = await service_gw.open_cif(
        cif_id=cif_id,
        customer_info=customer_info,
        account_info=account_info,
        current_user=current_user
    )

    if not response_data.get('openCIFAuthorise_out', {}).get('data_output') or not is_success:
        transaction_job.update({
            "complete_flag": False,
            "error_code": ERROR_OPEN_CIF,
            "error_desc": response_data.get('openCIFAuthorise_out', {}).get('transaction_info', {}).get('transaction_error_msg')
        })
    # insert transaction_job
    session.execute(
        insert(
            TransactionJob
        ).values(transaction_job)
    )
    session.commit()

    return ReposReturn(data=(is_success, response_data))


@auto_commit
async def repos_update_cif_number_customer(
        cif_id: str,
        data_update_customer: dict,
        data_update_casa_account: dict,
        session: Session
):
    session.execute(
        update(
            Customer
        ).filter(Customer.id == cif_id).values(data_update_customer)
    )

    if data_update_casa_account:
        session.execute(
            update(
                CasaAccount
            ).filter(CasaAccount.customer_id == cif_id).values(data_update_casa_account)
        )

    return ReposReturn(data=cif_id)


async def repos_get_casa_account(
        cif_id: str,
        session: Session
):
    casa_account = session.execute(
        select(
            CasaAccount
        ).filter(CasaAccount.customer_id == cif_id)
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
        .join(CustomerProfessional, Customer.customer_professional_id == CustomerProfessional.id)
        .join(AverageIncomeAmount, CustomerProfessional.average_income_amount_id == AverageIncomeAmount.id)
        .filter(Customer.id == cif_id)
    ).all()

    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA)

    return ReposReturn(data=customer)
