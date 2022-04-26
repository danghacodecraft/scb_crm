from sqlalchemy import CLOB, VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class News(Base):
    __tablename__ = 'crm_news'

    id = Column('news_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động tin tức')
    title = Column('title', VARCHAR(1000), nullable=False, comment='Tiêu đề tin tức')
    avatar_uuid = Column(VARCHAR(36), comment='Avatar uuid')
    thumbnail_uuid = Column(VARCHAR(36), comment='Banner tin tức')
    category_id = Column(ForeignKey('crm_news_category.news_category_id'))
    user_id = Column('user_id', VARCHAR(36), comment='Mã user tạo tin')
    user_name = Column('user_name', VARCHAR(255), comment='Tên user tạo tin')
    content = Column('content', CLOB, comment='Nội dung tin tức')
    total_comment = Column('total_comment', NUMBER(8, 0), comment='Tổng số coment')
    summary = Column('summary', VARCHAR(2000), comment='Tóm tắt nội dung tin tức')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')
    start_date = Column('start_date', DateTime, nullable=False, comment='Ngày bắt đầu')
    expired_date = Column('expired_date', DateTime, comment='Ngày hết hạn')
    active_flag = Column('active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')

    category = relationship('NewsCategory')


class NewsComment(Base):
    __tablename__ = 'crm_news_comment'

    id = Column('comment_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động bình luận')
    news_id = Column(ForeignKey('crm_news.news_id'))
    content = Column('content', VARCHAR(500), nullable=False, comment='Nội dung comment')
    parent_id = Column('comment_parent_id', VARCHAR(36), comment='id comment cha')
    create_user_id = Column('created_user_id', VARCHAR(10), nullable=False, comment='Mã user tạo comment')
    create_user_username = Column('created_user_username', VARCHAR(100), nullable=False,
                                  comment='Tên nick name tạo comment')
    create_user_name = Column('created_user_name', VARCHAR(50), nullable=False, comment='Tên user tạo comment')
    total_likes = Column('total_likes', NUMBER, nullable=False, comment="Số lượt like")
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')

    news = relationship('News')


class CommentLike(Base):
    __tablename__ = 'crm_news_comment_like'

    id = Column('like_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động')
    comment_id = Column(ForeignKey('crm_news_comment.comment_id'))
    create_user_id = Column('created_user_id', VARCHAR(36), nullable=False, comment='Mã user đã like')
    create_user_name = Column('created_user_name', VARCHAR(255), nullable=False, comment='Tên user like')
    create_user_username = Column('created_user_username', VARCHAR(255), nullable=False,
                                  comment='Tên nick name đã like')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')

    comment = relationship('NewsComment')
