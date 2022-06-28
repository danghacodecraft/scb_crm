from typing import Optional

from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.api.v1.endpoints.casa.pay_in_cash.schema import PayInCashRequest


async def repos_save_pay_in_cash_info(cif_number: Optional[str], request: PayInCashRequest, session: Session):
    pay_in_cash_info = dict()
    return ReposReturn(data=pay_in_cash_info)
