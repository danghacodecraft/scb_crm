from sqlalchemy import VARCHAR, Column, ForeignKey, text
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base


class ProductFeeCategory(Base):
    __tablename__ = 'crm_product_fee_category'

    id = Column('category_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã loại phí')
    code = Column('category_code', VARCHAR(50), comment='Mã loại phí')
    name = Column('category_name', VARCHAR(255), comment='Tên loại phí')


class ProductFee(Base):
    __tablename__ = 'crm_product_fee'

    id = Column('product_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='Mã phí')
    code = Column('product_code', VARCHAR(50), comment='Mã phí')
    name = Column('product_name', VARCHAR(255), comment='Tên phí')
    category_id = Column('product_category_id', ForeignKey('crm_product_fee_category.category_id'), comment='Mã loại phí')

    category = relationship('ProductFeeCategory')
