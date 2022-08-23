from cx_Oracle import NUMBER
from sqlalchemy import VARCHAR, Column, text

from app.third_parties.oracle.base import Base


class Tablet(Base):
    __tablename__ = 'crm_template'
    id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    template_id = Column(NUMBER(19), comment='id của template bên TMS', nullable=False)
    slug = Column(VARCHAR(300), comment='slug template', nullable=False)
    url_template = Column(VARCHAR(500), comment='url biểu mẫu', nullable=False)
    business_type_id = Column(VARCHAR(36), comment='Mã nghiệp vụ', nullable=False)
