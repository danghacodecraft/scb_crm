from cx_Oracle import NCLOB
from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.news import \
    NewsCategory  # noqa


class News(Base):
    __tablename__ = 'crm_news'

    id = Column('news_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động tin tức')
    title = Column('title', VARCHAR(1000), nullable=False, comment='Tiêu đề tin tức')
    avatar_uuid = Column('avatar_url', VARCHAR(36), comment='Tiêu đề tin tức')
    thumbnail_uuid = Column('thumbnail_url', VARCHAR(36), comment='Banner tin tức')
    category_id = Column(ForeignKey('crm_news_category.news_category_id'))
    user_id = Column('user_id', VARCHAR(36), comment='Mã user tạo tin')
    user_name = Column('user_name', VARCHAR(255), comment='Tên user tạo tin')
    content = Column('content', NCLOB, comment='Nội dung tin tức')
    summary = Column('summary', VARCHAR(2000), comment='Tóm tắt nội dung tin tức')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, comment='Ngày cập nhật')
    start_date = Column('start_date', DateTime, nullable=False, comment='Ngày bắt đầu')
    expired_date = Column('expired_date', DateTime, comment='Ngày hết hạn')
    active_flag = Column('active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')

    category = relationship('NewsCategory')
