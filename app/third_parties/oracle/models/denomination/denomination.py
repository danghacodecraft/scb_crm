from sqlalchemy import VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class CurrencyDenomination(Base):
    __tablename__ = 'crm_currency_denomination'

    id = Column('id', NUMBER, primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động bình luận'
                )
    currency_id = Column('currency_id', VARCHAR(5), comment='ID loại tiền')
    denominations = Column('currency_denominations', NUMBER, comment='Mệnh giá')
    denominations_name = Column('currency_denominations_name', VARCHAR(250), comment='Mệnh giá (bằng chữ)')
