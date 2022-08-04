from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.master_data.account import (
    AccountClass, AccountClassCurrency, AccountClassCustomerCategory,
    AccountClassType
)
from app.utils.error_messages import ERROR_ACCOUNT_CLASS_NOT_EXIST


async def repos_get_account_class(
        session: Session,
        customer_category_id: str,
        currency_id: str,
        account_type_id: str
):

    account_class = session.execute(
        select(
            AccountClass,
            AccountClassType,
            AccountClassCustomerCategory,
            AccountClassCurrency
        )
        .join(AccountClassType, and_(
            AccountClass.id == AccountClassType.account_class_id,
            AccountClassType.account_type_id == account_type_id
        ))
        .join(AccountClassCustomerCategory, and_(
            AccountClass.id == AccountClassCustomerCategory.account_class_id,
            AccountClassCustomerCategory.customer_category_id == customer_category_id
        ))
        .join(AccountClassCurrency, and_(
            AccountClass.id == AccountClassCurrency.account_class_id,
            AccountClassCurrency.currency_id == currency_id
        ))
    ).scalars().all()

    if not account_class:
        return ReposReturn(
            is_error=True,
            msg=ERROR_ACCOUNT_CLASS_NOT_EXIST,
            loc=f'account_type_id: {account_type_id}, '
                f'customer_category_id: {customer_category_id}, '
                f'currency_id: {currency_id}'
        )

    return ReposReturn(data=account_class)


async def repos_get_account_classes(
        session: Session,
        customer_category_id: str,
        account_class_ids: List[str]
):
    account_class = session.execute(
        select(
            AccountClass.id,
            AccountClassCustomerCategory,
        )
        .join(AccountClass, and_(
            AccountClassCustomerCategory.account_class_id == AccountClass.id,
            AccountClass.id.in_(account_class_ids)
        ))
        .filter(AccountClassCustomerCategory.customer_category_id == customer_category_id)
    ).scalars().all()
    return ReposReturn(data=account_class)
