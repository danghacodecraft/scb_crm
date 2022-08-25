from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.denomination.denomination import (
    CurrencyDenomination
)


async def repos_get_denominations(currency_id: str, session: Session) -> ReposReturn:
    denominations = session.execute(
        select(
            CurrencyDenomination
        ).filter(CurrencyDenomination.currency_id == currency_id)
        .order_by(CurrencyDenomination.denominations.desc())

    ).scalars().all()

    return ReposReturn(data=denominations)
