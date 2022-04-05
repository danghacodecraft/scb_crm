from datetime import datetime

from sqlalchemy import delete, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.third_parties.oracle.models.news.model import News
from app.utils.error_messages import ERROR_ID_NOT_EXIST


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
    try:
        obj = session.execute(select(News, NewsCategory)
                              .join(NewsCategory, NewsCategory.id == News.category_id).filter(News.id == news_id)).one()
    except Exception:
        return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc="news_id")

    return ReposReturn(data=obj)


async def get_list_scb_news(
        session: Session,
        title: str,
        category_news: str,
        start_date: datetime,
        expired_date: datetime,
        active_flag: int,
        limit: int,
        page: int,
) -> ReposReturn:
    query_data = select(
        News,
        NewsCategory
    ).join(NewsCategory, NewsCategory.id == News.category_id)
    if title:
        query_data = query_data.filter(News.title.ilike(f'%{title}%'))
    if category_news:
        query_data = query_data.filter(News.category_id == category_news)
    if start_date:
        query_data = query_data.filter(News.start_date == start_date)
    if expired_date:
        query_data = query_data.filter(News.expired_date == expired_date)
    if active_flag:
        query_data = query_data.filter(News.active_flag == active_flag)
    total_row = session.execute(query_data).all()
    query_data = query_data.limit(limit)
    query_data = query_data.offset(limit * (page - 1))

    query_data = session.execute(
        query_data.order_by(desc(News.created_at))).all()

    return ReposReturn(data={
        "query_data": query_data,
        "total_row": total_row
    })
