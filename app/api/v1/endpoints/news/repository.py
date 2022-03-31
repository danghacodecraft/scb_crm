from sqlalchemy import delete, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.third_parties.oracle.models.news.model import News
from app.utils.error_messages import ERROR_ID_NOT_EXIST, ERROR_NO_DATA


@auto_commit
async def repos_add_scb_news(
        data_scb_news,
        session: Session) -> ReposReturn:

    session.add(News(**data_scb_news))
    return ReposReturn(data=data_scb_news)


@auto_commit
async def repos_update_scb_news(
        news_id,
        data_scb_news,
        session: Session) -> ReposReturn:

    session.execute(delete(News).filter(News.id == news_id))
    session.add(News(**data_scb_news))
    return ReposReturn(data=data_scb_news)


async def get_data_by_id(session: Session, news_id: str) -> ReposReturn:
    obj = session.execute(select(News, NewsCategory)
                          .join(NewsCategory, NewsCategory.id == News.category_id).filter(News.id == news_id)).one()
    if not obj:
        return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc="news_id")

    return ReposReturn(data=obj)


async def get_list_scb_news(session: Session) -> ReposReturn:
    query_data = session.execute(
        select(
            News,
            NewsCategory
        ).join(NewsCategory, NewsCategory.id == News.category_id).order_by(desc(News.created_at))).all()
    if not query_data:
        return ReposReturn(is_error=True, msg=ERROR_NO_DATA, loc="Null data")

    return ReposReturn(data=query_data)
