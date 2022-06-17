from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.account import AccountClass, AccountClassCustomerCategory


async def repos_get_account_class(session: Session, customer_category_id: Optional[str] = None):
    raw_sql = select(
            AccountClass,
            AccountClassCustomerCategory,
        )\
        .join(AccountClass, AccountClassCustomerCategory.account_class_id == AccountClass.id)
    if customer_category_id:
        raw_sql = raw_sql.filter(AccountClassCustomerCategory.customer_category_id == customer_category_id)
    account_class = session.execute(raw_sql).scalars().all()
    return ReposReturn(data=account_class)
