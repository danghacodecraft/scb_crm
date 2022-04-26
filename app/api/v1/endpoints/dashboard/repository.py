from typing import Optional

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
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
    Booking, BookingCustomer
)
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.cif import CONTACT_ADDRESS_CODE
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


async def repos_count_total_item(search_box: str, session: Session) -> ReposReturn:
    transaction_list = select(
        func.count(Booking.code)
    ) \
        .join(BookingCustomer, Booking.id == BookingCustomer.booking_id) \
        .join(Customer, BookingCustomer.customer_id == Customer.id) \
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)

    if search_box:
        search_box = f'%{search_box}%'
        transaction_list = transaction_list.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    CustomerIdentity.identity_num.ilike(search_box),
                ),
                or_(
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                ),
                or_(
                    Customer.cif_number.ilike(search_box)
                )
            )
        )

    total_item = session.execute(transaction_list).scalar()
    return ReposReturn(data=total_item)


async def repos_get_transaction_list(search_box: Optional[str], limit: int, page: int, session: Session):
    sql = select(
        Customer.full_name_vn,
        Customer.id.label('cif_id'),
        Booking.code.label('booking_code')
    ) \
        .join(BookingCustomer, Customer.id == BookingCustomer.customer_id) \
        .join(Booking, BookingCustomer.booking_id == Booking.id) \
        .limit(limit) \
        .offset(limit * (page - 1)) \
        .order_by(desc(Customer.open_cif_at))

    if search_box:
        search_box = f'%{search_box}%'
        sql = sql.filter(
            or_(
                Booking.code.ilike(search_box),
                or_(
                    CustomerIdentity.identity_num.ilike(search_box),
                ),
                or_(
                    Customer.full_name.ilike(convert_to_unsigned_vietnamese(search_box))
                ),
                or_(
                    Customer.cif_number.ilike(search_box)
                )
            )
        )

    transaction_list = session.execute(sql).all()
    return ReposReturn(data=transaction_list)


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
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .join(CustomerAddress,
              and_(
                  Customer.id == CustomerAddress.customer_id,
                  CustomerAddress.address_type_id == CONTACT_ADDRESS_CODE
              )) \
        .join(AddressWard, CustomerAddress.address_ward_id == AddressWard.id) \
        .join(AddressDistrict, CustomerAddress.address_district_id == AddressDistrict.id) \
        .join(AddressProvince, CustomerAddress.address_province_id == AddressProvince.id) \
        .join(AddressCountry, CustomerAddress.address_country_id == AddressCountry.id) \
        .join(Branch, Customer.open_branch_id == Branch.id)

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
        .join(Branch, Customer.open_branch_id == Branch.id)

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
