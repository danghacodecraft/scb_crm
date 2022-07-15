from sqlalchemy import select
from sqlalchemy.orm import Session

from app.third_parties.oracle.models.cif.basic_information.guardian_and_relationship.model import (
    CustomerPersonalRelationship
)


async def repos_get_customer_personal_relationships(
        session: Session,
        relationship_type: int,
        cif_id: str
):
    return session.execute(
        select(
            CustomerPersonalRelationship
        ).filter(
            CustomerPersonalRelationship.type == relationship_type,
            CustomerPersonalRelationship.customer_id == cif_id
        )).scalars().all()
