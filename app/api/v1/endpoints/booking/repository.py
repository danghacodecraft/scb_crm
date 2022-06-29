from sqlalchemy import asc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.other_information.model import Comment


@auto_commit
async def repo_add_comment(data_comment,
                           session: Session) -> ReposReturn:
    session.add(Comment(**data_comment))
    return ReposReturn(data=data_comment)


async def get_list_comment(session: Session, booking_id: str) -> ReposReturn:
    query = session.execute(
        select(
            Comment
        ).filter(
            Comment.booking_id == booking_id
        ).order_by(asc(Comment.created_at))
    ).scalars()

    return ReposReturn(data=query)
