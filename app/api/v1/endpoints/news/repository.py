from datetime import datetime

from sqlalchemy import and_, delete, desc, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.master_data.news import NewsCategory
from app.third_parties.oracle.models.news.model import (
    CommentLike, News, NewsComment
)
from app.utils.constant.cif import NEWS_COMMENT_FILTER_BY_INTERESTED
from app.utils.error_messages import ERROR_ID_NOT_EXIST, USER_CODE_NOT_EXIST
from app.utils.functions import now


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
    obj = session.execute(select(News).filter(News.id == news_id)).one()

    obj.News.title = data_scb_news['title']
    obj.News.avatar_uuid = data_scb_news['avatar_uuid']
    obj.News.category_id = data_scb_news['category_id']
    obj.News.user_id = data_scb_news['user_id']
    obj.News.user_name = data_scb_news['user_name']
    obj.News.content = data_scb_news['content']
    obj.News.summary = data_scb_news['summary']
    obj.News.start_date = data_scb_news['start_date']
    obj.News.expired_date = data_scb_news['expired_date']
    obj.News.active_flag = data_scb_news['active_flag']
    obj.News.updated_at = data_scb_news['updated_at']

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
    if active_flag is not None:
        query_data = query_data.filter(News.active_flag == active_flag)
    if start_date and expired_date:
        query_data = query_data.filter(News.created_at.between(start_date, expired_date))
    if not start_date and expired_date:
        query_data = query_data.filter(News.created_at <= expired_date)
    if start_date and not expired_date:
        query_data = query_data.filter(News.created_at.between(start_date, now()))

    total_row = session.execute(query_data).all()
    query_data = query_data.limit(limit)
    query_data = query_data.offset(limit * (page - 1))

    query_data = session.execute(
        query_data.order_by(desc(News.created_at))).all()

    return ReposReturn(data={
        "query_data": query_data,
        "total_row": total_row
    })


@auto_commit
async def repo_add_comment(data_comment,
                           news_id,
                           session: Session) -> ReposReturn:
    obj = session.execute(select(News).filter(News.id == news_id)).first()
    obj.News.total_comment += 1
    session.add(NewsComment(**data_comment))
    return ReposReturn(data=data_comment)


async def get_list_comment(session: Session, news_id: str, filter_by: str, page: int) -> ReposReturn:
    # Querry list comment cha
    query = select(NewsComment).filter(and_(NewsComment.news_id == news_id, NewsComment.parent_id == None))  # noqa
    if filter_by == NEWS_COMMENT_FILTER_BY_INTERESTED:
        query = query.order_by(desc(NewsComment.total_likes))
    else:
        query = query.order_by(desc(NewsComment.created_at))

    total_comment_parent = session.execute(query).all()
    query = query.limit(page * 10)
    query = query.offset(0)
    objs = session.execute(query).scalars().all()

    # Querry list comment con
    cmt_parent_ids = []
    for item in objs:
        cmt_parent_ids.append(item.id)

    query_cmt_child = select(NewsComment).filter(
        and_(NewsComment.news_id == news_id, NewsComment.parent_id.in_(cmt_parent_ids)))
    objs_child = session.execute(query_cmt_child).scalars().all()

    return ReposReturn(data={
        "total_comment_parent": total_comment_parent,
        "list_comment": objs,
        "list_child_comment": objs_child
    })


async def get_comment_by_id(session: Session, comment_id: str):
    try:
        cmt_obj = session.execute(select(NewsComment).filter(NewsComment.id == comment_id)).one()
    except Exception:
        return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc="comment_id")

    return ReposReturn(data=cmt_obj)


async def get_like_by_user(session: Session, user_id: str, comment_id: str):
    cmt_obj = session.execute(
        select(CommentLike).filter(
            and_(CommentLike.comment_id == comment_id, CommentLike.create_user_id == user_id))).first()

    return ReposReturn(data=cmt_obj)


@auto_commit
async def repo_add_comment_like(comment_id, like_data, session: Session) -> ReposReturn:
    cmt_obj = session.execute(select(NewsComment).filter(NewsComment.id == comment_id)).first()
    cmt_obj.NewsComment.total_likes += 1

    session.add(CommentLike(**like_data))
    return ReposReturn(data=cmt_obj.NewsComment.total_likes)


@auto_commit
async def repo_remove_comment_like(comment_id, like_id, session: Session) -> ReposReturn:
    cmt_obj = session.execute(select(NewsComment).filter(NewsComment.id == comment_id)).first()
    cmt_obj.NewsComment.total_likes -= 1

    session.execute(delete(CommentLike).filter(CommentLike.id == like_id))

    return ReposReturn(data=cmt_obj.NewsComment.total_likes)


async def repo_get_users_contact(codes, session: Session):
    sql_contact = f"""SELECT HRM_EMPLOYEE.EMP_NAME,\
       HRM_EMPLOYEE.EMP_CODE,\
       HRM_EMPLOYEE.USERNAME,\
       HRM_EMPLOYEE.WORKING_LOCATION,\
       HRM_EMPLOYEE.EMAIL_SCB,\
       HRM_EMPLOYEE.CONTACT_MOBILE,\
       HRM_EMPLOYEE.INTERNAL_MOBILE,\
       HRM_EMPLOYEE.ID      AS EMP_ID,\
       HRM_TITLE.TITLE_NAME  AS TITLE_NAME,\
       HRM_ORGANIZATION.DESCRIPTION_PATH     AS UNIT,\
       CONCAT('/cdn-profile/', HRM_EMPLOYEE.AVATAR_URL) AS AVATAR_LINK FROM HRM_EMPLOYEE\

        LEFT OUTER JOIN HRM_TITLE ON (HRM_EMPLOYEE.TITLE_ID = HRM_TITLE.ID)
        LEFT OUTER JOIN HRM_ORGANIZATION ON (HRM_EMPLOYEE.ORG_ID = HRM_ORGANIZATION.ID)
        WHERE HRM_EMPLOYEE.EMP_CODE IN {codes}
        ORDER BY HRM_EMPLOYEE.USERNAME ASC"""
    try:
        data_contact = session.execute(sql_contact).all()
    except NoResultFound:
        return ReposReturn(is_error=True, loc='user_code', msg=USER_CODE_NOT_EXIST,
                           detail="Contact -> user_code")
    except Exception as ex:
        return ReposReturn(is_error=True, msg=str(ex))

    return ReposReturn(data=data_contact)


async def get_comment_like_by_user(session: Session, comment_ids: list, user_id: str):
    query_data = select(CommentLike.comment_id).filter(and_(CommentLike.comment_id.in_(comment_ids),
                                                            CommentLike.create_user_id == user_id))  # noqa

    cmts_data = session.execute(query_data).scalars().all()

    return ReposReturn(data=cmts_data)


async def get_parent_comment(session: Session, news_id: str, comment_id: str):
    try:
        query_data = select(NewsComment).filter(and_(NewsComment.news_id == news_id,
                                                     NewsComment.id == comment_id,
                                                     NewsComment.parent_id == None))  # noqa
        data = session.execute(query_data).one()
    except Exception:
        return ReposReturn(is_error=True, msg=ERROR_ID_NOT_EXIST, loc="parent_id")

    return ReposReturn(data=data)
