from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.eKYC.model import Statistic


@auto_commit
async def repos_create_ekyc_customer(customer: dict, session: Session):
    session.add(Statistic(**customer))
    session.flush()
    return ReposReturn(data=None)


@auto_commit
async def repos_update_ekyc_customer(customer, customer_id: str, session: Session):
    session.execute(
        update(
            Statistic
        )
        .filter(Statistic.customer_id == customer_id)
        .values(**customer)
    )
    session.flush()
    return ReposReturn(data=None)


async def repos_get_ekyc_customer(customer_id: str, session: Session):
    return ReposReturn(data=session.execute(
        select(
            Statistic
        )
        .filter(Statistic.customer_id == customer_id)
    ).scalar())
