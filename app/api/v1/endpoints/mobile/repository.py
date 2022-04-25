from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer
)


async def repos_get_total_item(
        search_box: str,
        session: Session
):
    identity = select(
        func.count(Customer.id)
    ) \
        .join(CustomerIdentity, CustomerIdentity.customer_id == Customer.id) \
        .join(BookingCustomer, BookingCustomer.customer_id == Customer.id) \
        .join(Booking, Booking.id == BookingCustomer.booking_id)

    if search_box:
        identity = identity.filter(
            or_(
                CustomerIdentity.identity_num.ilike(f'%{search_box}%'),
                Customer.full_name.ilike(f'%{search_box}%'),
                Customer.full_name_vn.ilike(f'%{search_box}%'),
                Booking.code.ilike(f'%{search_box}%')
            )
        )
    identity = session.execute(identity).scalar()

    return ReposReturn(data=identity)


async def repos_get_mobile_identity(
        search_box: str,
        limit: int,
        page: int,
        session: Session
):
    identity = select(
        Customer,
        CustomerIdentity,
        BookingCustomer,
        Booking
    ) \
        .join(CustomerIdentity, CustomerIdentity.customer_id == Customer.id) \
        .join(BookingCustomer, BookingCustomer.customer_id == Customer.id) \
        .join(Booking, Booking.id == BookingCustomer.booking_id)

    if search_box:
        identity = identity.filter(
            or_(
                CustomerIdentity.identity_num.ilike(f'%{search_box}%'),
                Customer.full_name.ilike(f'%{search_box}%'),
                Customer.full_name_vn.ilike(f'%{search_box}%'),
                Booking.code.ilike(f'%{search_box}%')
            )
        )

    identity = identity.limit(limit)
    identity = identity.offset(limit * (page - 1))
    identity = session.execute(identity).all()

    return ReposReturn(data=identity)
