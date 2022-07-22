from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.eKYC.model import Statistic


@auto_commit
async def repos_create_ekyc_customer(customer: dict, session: Session):
    session.add(Statistic(**customer))
    session.flush()
    return ReposReturn(data=None)
