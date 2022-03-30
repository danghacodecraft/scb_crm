from sqlalchemy import VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class NewsCategory(Base):
    __tablename__ = 'crm_news_category'

    id = Column('news_category_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='ID Mã chuyên mục')
    code = Column('news_category_code', VARCHAR(50), nullable=False, comment='Mã chuyên mục')
    name = Column('news_category_name', VARCHAR(255), nullable=False, comment='Tên chuyên mục')
    active_flag = Column('active_flag', NUMBER(1, 0, False), nullable=False, comment='Trạng thái hoạt động')
    order_no = Column('order_no', NUMBER(3, 0, False), comment='Sắp xếp')
