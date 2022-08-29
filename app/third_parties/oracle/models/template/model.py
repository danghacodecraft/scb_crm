from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, text

from app.third_parties.oracle.base import Base


class Template(Base):
    __tablename__ = 'crm_template'
    id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    template_id = Column("template_id", Integer, comment='id của template bên TMS', nullable=False)
    name = Column("template_name", VARCHAR(300), comment='tên của template bên TMS', nullable=False)
    slug = Column('template_slug', VARCHAR(300), comment='slug template', nullable=False)
    template_url = Column(VARCHAR(500), comment='url biểu mẫu', nullable=False)
    business_type_id = Column('business_type_id', ForeignKey('crm_business_type.business_type_id'),
                              comment='ID type')
