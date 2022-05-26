from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.other_information.model import Comment


@auto_commit
async def repo_add_comment(data_comment,
                           session: Session) -> ReposReturn:
    session.add(Comment(**data_comment))
    return ReposReturn(data=data_comment)
