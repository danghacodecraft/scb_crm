from sqlalchemy import VARCHAR, Column, text

from app.third_parties.oracle.base import Base


class ProductFeeCategory(Base):
    __tablename__ = 'crm_product_fee_category'

    id = Column('category_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã phí')
    code = Column('category_code', VARCHAR(50), comment='Mã phí')
    name = Column('category_name', VARCHAR(255), comment='Tên phí')
