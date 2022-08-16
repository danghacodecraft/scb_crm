from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.blacklist.model import Blacklist


@auto_commit
async def repo_add_blacklist(data_blacklist,
                             session: Session) -> ReposReturn:
    session.add(Blacklist(**data_blacklist))
    return ReposReturn(data=data_blacklist)


async def repo_view_blacklist(session: Session,
                              limit: int,
                              page: int,
                              data_filter: dict = {},
                              ):
    black_list = select(
        Blacklist
    )
    black_list = black_list.filter_by(**data_filter)

    black_list = black_list.limit(limit)
    black_list = black_list.offset(limit * (page-1))

    black_list = session.execute(black_list).all()

    return ReposReturn(data=black_list)
