from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.document_file.model import DocumentFile


async def repos_count_document_item(booking_id, session: Session) -> ReposReturn:
    total_item = session.execute(
        select(
            func.count(DocumentFile.id)
        ).filter(DocumentFile.booking_id == booking_id)

    ).scalar()
    return ReposReturn(data=total_item)


async def repos_get_document_list(
        booking_id: str,
        limit: int,
        page: int,
        session: Session
):
    document_list = session.execute(
        select(
            DocumentFile
        ).filter(DocumentFile.booking_id == booking_id)
        .limit(limit)
        .offset(limit * (page - 1))
        .order_by(desc(DocumentFile.created_at))
    ).scalars().all()

    return ReposReturn(data=document_list)
