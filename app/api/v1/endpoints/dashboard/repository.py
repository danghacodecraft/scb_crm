from sqlalchemy import and_, desc, or_, select
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


async def repos_get_transaction_list(search_box: str, session: Session):
    if not search_box:
        transaction_list = session.execute(
            select(
                Customer
            )
            .order_by(desc(Customer.open_cif_at))
        ).scalars().all()
    else:
        transaction_list = session.execute(
            select(
                CustomerIdentity,
                Customer
            )
            .join(Customer, CustomerIdentity.customer_id == Customer.id)
            .filter(
                or_(
                    CustomerIdentity.identity_num.like('%' + search_box + '%'),
                    or_(
                        Customer.full_name.like('%' + search_box.upper() + '%')
                    ),
                    or_(
                        Customer.cif_number.like('%' + search_box + '%')
                    )
                ))
            .order_by(desc(Customer.open_cif_at))
        ).all()

    return ReposReturn(data=transaction_list)


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
        # count(Customer.id).over().label("total"),
    )\
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id) \
        .join(CustomerAddress, and_(
            Customer.id == CustomerAddress.customer_id,
            CustomerAddress.address_type_id == "TAM_TRU"
        )
    )

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

    customer = session.execute(
        customers.order_by(desc('open_cif_at')),
    ).all()

    return ReposReturn(data=customer)
