from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class DBS(Base):
    __tablename__ = 'env_global_system'
    name = Column(VARCHAR(50), primary_key=True)
    value = Column(VARCHAR(255), nullable=True)
    is_server = Column(NUMBER(1), nullable=True)
    server_name = Column(VARCHAR(50), nullable=True)
