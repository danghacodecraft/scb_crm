from datetime import date
from typing import Optional

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_dwh
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import (
    Branch, BusinessType, TransactionStage, TransactionStageRole,
    TransactionStageStatus
)
from app.utils.constant.cif import CONTACT_ADDRESS_CODE
from app.utils.constant.dwh import NAME_ACCOUNTING_ENTRY
from app.utils.functions import date_to_datetime, end_time_of_day
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


async def repos_count_total_item(region_id: Optional[str], branch_id: Optional[str], transaction_type_id: Optional[str],
                                 status_code: Optional[str], search_box: Optional[str], from_date: Optional[date],
                                 to_date: Optional[date], session: Session) -> ReposReturn:
    transaction_list = select(
        func.count(Booking.code)
    ) \
        .join(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .join(Customer, BookingCustomer.customer_id == Customer.id) \
        .join(Branch, Booking.branch_id == Branch.id) \
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id) \
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .join(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)

    if region_id:
        transaction_list = transaction_list.filter(Branch.region_id == region_id)

    if branch_id:
        transaction_list = transaction_list.filter(Booking.branch_id == branch_id)

    if transaction_type_id:
        transaction_list = transaction_list.filter(Booking.business_type_id == transaction_type_id)

    if status_code:
        transaction_list = transaction_list.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        transaction_list = transaction_list.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date and to_date:
        transaction_list = transaction_list.filter(
            and_(
                Booking.created_at >= date_to_datetime(from_date),
                Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
            ))

    total_item = session.execute(transaction_list).scalar()
    return ReposReturn(data=total_item)


async def repos_get_transaction_list(region_id: Optional[str], branch_id: Optional[str],
                                     transaction_type_id: Optional[str], status_code: Optional[str],
                                     search_box: Optional[str], from_date: Optional[date], to_date: Optional[date],
                                     limit: int, page: int, session: Session):
    sql = select(
        Customer.full_name_vn,
        Customer.id.label('cif_id'),
        Customer.cif_number,
        Booking.id,
        Booking.code.label('booking_code'),
        TransactionStageStatus.name.label('status'),
        BusinessType.id.label('business_type_id'),
        BusinessType.name.label('business_type_name'),
        Branch.code.label('branch_code'),
        Branch.name.label('branch_name')
    ) \
        .join(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .outerjoin(Customer, BookingCustomer.customer_id == Customer.id) \
        .outerjoin(BusinessType, Booking.business_type_id == BusinessType.id) \
        .outerjoin(Branch, Booking.branch_id == Branch.id) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .outerjoin(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id) \
        .outerjoin(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id) \
        .outerjoin(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id) \
        .filter(Booking.code.is_not(None)) \
        .limit(limit) \
        .offset(limit * (page - 1)) \
        .order_by(desc(Customer.open_cif_at))

    if region_id:
        sql = sql.filter(Branch.region_id == region_id)

    if branch_id:
        sql = sql.filter(Booking.branch_id == branch_id)

    if transaction_type_id:
        sql = sql.filter(Booking.business_type_id == transaction_type_id)

    if status_code:
        sql = sql.filter(TransactionStageStatus.code == status_code)

    if search_box:
        search_box = f'%{search_box}%'
        sql = sql.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    Customer.cif_number.ilike(search_box),
                    or_(
                        CustomerIdentity.identity_num.ilike(search_box)),
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                )
            )
        )

    if from_date and to_date:
        sql = sql.filter(
            and_(
                Booking.created_at >= date_to_datetime(from_date),
                Booking.created_at <= end_time_of_day(date_to_datetime(to_date))
            ))

    transaction_list = session.execute(sql).all()
    return ReposReturn(data=transaction_list)


async def repos_get_senders(
        booking_ids: tuple,
        session: Session
):
    senders = session.execute(
        select(
            Customer,
            TransactionStage,
            TransactionStageRole,
            TransactionSender,
            BookingCustomer,
            Booking,
            TransactionDaily
        )
        .join(Customer, BookingCustomer.customer_id == Customer.id)
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .outerjoin(TransactionStageRole, TransactionStage.id == TransactionStageRole.transaction_stage_id)
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .filter(BookingCustomer.booking_id.in_(booking_ids))
    ).all()
    return ReposReturn(data=senders)


async def repos_get_total_item(
        cif_number: str,
        identity_number: str,
        phone_number: str,
        full_name: str,
        session: Session
):
    customers = select(
        func.count(Customer.id)
    ) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .outerjoin(CustomerAddress,
                   and_(
                       Customer.id == CustomerAddress.customer_id,
                       CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
                   )) \
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id) \
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id) \
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id) \
        .outerjoin(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id) \
        .outerjoin(Branch, Customer.open_branch_id == Branch.id)

    customers = customers.filter(Customer.complete_flag == True)  # noqa
    if cif_number:
        customers = customers.filter(Customer.cif_number.ilike(f'%{cif_number}%'))
    if identity_number:
        customers = customers.filter(CustomerIdentity.identity_num.ilike(f'%{identity_number}%'))
    if phone_number:
        customers = customers.filter(Customer.mobile_number.ilike(f'%{phone_number}%'))
    if full_name:
        customers = customers.filter(Customer.full_name.ilike(f'%{full_name}%'))

    total_item = session.execute(
        customers
    ).scalar()

    return ReposReturn(data=total_item)


async def repos_get_customer(
        cif_number: str,
        identity_number: str,
        phone_number: str,
        full_name: str,
        limit: int,
        page: int,
        session: Session
):
    customers = select(
        Customer,
        CustomerIdentity,
        CustomerAddress,
        AddressWard,
        AddressDistrict,
        AddressProvince,
        AddressCountry,
        Branch
    ) \
        .outerjoin(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .outerjoin(CustomerAddress, and_(
            Customer.id == CustomerAddress.customer_id,
            CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
        )) \
        .outerjoin(AddressWard, CustomerAddress.address_ward_id == AddressWard.id) \
        .outerjoin(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id) \
        .outerjoin(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id) \
        .outerjoin(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id) \
        .outerjoin(Branch, Customer.open_branch_id == Branch.id)

    customers = customers.filter(Customer.complete_flag == True)  # noqa
    if cif_number:
        customers = customers.filter(Customer.cif_number.ilike(f'%{cif_number}%'))
    if identity_number:
        customers = customers.filter(CustomerIdentity.identity_num.ilike(f'%{identity_number}%'))
    if phone_number:
        customers = customers.filter(Customer.mobile_number.ilike(f'%{phone_number}%'))
    if full_name:
        customers = customers.filter(Customer.full_name.ilike(f'%{full_name}%'))

    customers = customers.limit(limit)
    customers = customers.offset(limit * (page - 1))

    customers = session.execute(
        customers.order_by(desc('open_cif_at')),
    ).all()

    return ReposReturn(data=customers)


async def repos_branch(
        branch_code: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.get_branch(branch_code=branch_code)

    return ReposReturn(data=data_response)


async def repos_accounting_entry(
        branch_code: str,
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.accounting_entry(branch_code=branch_code, module=NAME_ACCOUNTING_ENTRY)

    return ReposReturn(data=data_response)


async def repos_region(
        session: Session
) -> ReposReturn:
    data_response = await service_dwh.get_region()

    return ReposReturn(data=data_response)
