from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)


async def repos_check_account_num(account_num, session: Session) -> ReposReturn:
    account_info = session.execute(
        select(CasaAccount.casa_account_number)
        .filter(CasaAccount.casa_account_number == account_num)
    ).scalar()

    return ReposReturn(data=account_info)
