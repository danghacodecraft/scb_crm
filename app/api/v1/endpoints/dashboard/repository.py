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
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.cif import CONTACT_ADDRESS_CODE


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
        CustomerAddress,
        AddressWard,
        AddressDistrict,
        AddressProvince,
        AddressCountry,
        Branch
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

    # lấy tổng số item khi query
    total_item = session.execute(
        customers
    ).all()

    customers = customers.limit(limit)
    customers = customers.offset(limit * (page - 1))

    customers = session.execute(
        customers.order_by(desc('open_cif_at')),
    ).all()

    return ReposReturn(data=(len(total_item), customers))
