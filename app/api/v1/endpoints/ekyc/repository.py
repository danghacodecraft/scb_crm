from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.eKYC.model import (
    EKYCCustomer, EKYCCustomerStep
)
from app.utils.functions import now


@auto_commit
async def repos_create_ekyc_customer(customer: dict, steps, session: Session):
    insert_list = [EKYCCustomer(**customer)]
    if steps:
        for step in steps:
            insert_list.append(EKYCCustomerStep(**step))
    session.add_all(insert_list)
    session.flush()
    return ReposReturn(data=None)


@auto_commit
async def repos_update_ekyc_customer(
        step_info: dict,
        update_customer_info: dict,
        session: Session
):
    session.add(EKYCCustomerStep(**step_info))
    if update_customer_info:
        update_customer_info.update(
            updated_at=now()
        )
        session.execute(
            update(EKYCCustomer)
            .filter(EKYCCustomer.customer_id == step_info['customer_id'])
            .values(**update_customer_info)
        )
    session.flush()
    return ReposReturn(data=None)


async def repos_get_ekyc_customer(customer_ekyc_id: str, session: Session):
    customer_ekyc = session.execute(
        select(
            EKYCCustomer
        )
        .filter(EKYCCustomer.customer_id == customer_ekyc_id)
    ).scalar()

    return ReposReturn(data=customer_ekyc)


@auto_commit
async def repos_update_ekyc_customer_kss(update_customer_ekyc_kss, session: Session):
    session.execute(
        update(EKYCCustomer).values(update_customer_ekyc_kss)
    )
    return ReposReturn(data=None)
