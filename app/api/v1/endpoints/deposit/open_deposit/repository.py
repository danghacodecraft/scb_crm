from typing import List

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.e_banking.model import (
    TdAccount, TdAccountResign
)


@auto_commit
async def repos_save_td_account(
        td_accounts: List,
        td_account_resigns: List,
        session: Session
):
    session.bulk_save_objects([TdAccount(**item) for item in td_accounts])

    session.bulk_save_objects([TdAccountResign(**item) for item in td_account_resigns])

    return ReposReturn(data='td_account')
