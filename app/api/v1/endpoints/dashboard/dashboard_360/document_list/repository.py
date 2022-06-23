from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.basic_information.model import Customer
from app.third_parties.oracle.models.document_file.model import DocumentFile


async def repos_count_document_item(cif_number, session: Session) -> ReposReturn:
    total_item = session.execute(
        select(
            DocumentFile,
            Customer
        )
        .join(DocumentFile, Customer.id == DocumentFile.customer_id)
        .filter(Customer.cif_number == cif_number)

    ).scalars().all()

    total_item = len(total_item)

    return ReposReturn(data=total_item)


async def repos_get_document_list(
        cif_number: str,
        limit: int,
        page: int,
        session: Session
):
    document_list = session.execute(
        select(
            DocumentFile,
            Customer
        )
        .join(DocumentFile, Customer.id == DocumentFile.customer_id)
        .filter(Customer.cif_number == cif_number)
        .limit(limit)
        .offset(limit * (page - 1))
        .order_by(desc(DocumentFile.created_at))
    ).scalars().all()

    return ReposReturn(data=document_list)
