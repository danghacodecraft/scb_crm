
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.debit_card.model import (
    CardDeliveryAddress
)
from app.utils.functions import now


@auto_commit
async def repos_add_scb_news(
        data_scb_news,
        session: Session) -> ReposReturn:
    session.add(CardDeliveryAddress(**data_scb_news))
    session.flush()

    return ReposReturn(data={
        "cif_id": "cif_id",
        'created_at': now(),
        'created_by': 'system',
        'updated_at': now(),
        'updated_by': 'system'
    })
