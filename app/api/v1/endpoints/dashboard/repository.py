from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
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
