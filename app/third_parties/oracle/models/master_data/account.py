from sqlalchemy import VARCHAR, Column, ForeignKey, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.customer import \
    CustomerCategory  # noqa
from app.third_parties.oracle.models.master_data.others import Currency  # noqa


class AccountClass(Base):
    __tablename__ = 'crm_acc_class'
    __table_args__ = {'comment': 'Loại hình tài khoản'}

    id = Column('acc_class_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Loại hình tài khoản')
    code = Column('acc_class_code', VARCHAR(50), nullable=False, comment='Mã code Loại hình tài khoản')
    name = Column('acc_class_name', VARCHAR(255), nullable=False, comment='Tên Loại hình tài khoản')


class AccountStructureType(Base):
    __tablename__ = 'crm_acc_structure_type'
    __table_args__ = {'comment': 'Loại kết cấu tài khoản'}

    id = Column('acc_structure_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã loại kết cấu tài khoản')
    parent_id = Column('acc_structure_type_parent_id', VARCHAR(36), comment='Mã cấp cha loại kết cấu tài khoản')
    code = Column('acc_structure_type_code', VARCHAR(50), comment='Mã code loại kết cấu tài khoản')
    name = Column('acc_structure_type_name', VARCHAR(255), comment='Tên loại kết cấu tài khoản')
    value = Column('acc_structure_type_value', VARCHAR(16), comment='Giá trị loại kết cấu tài khoản')
    level = Column('acc_structure_type_level', NUMBER(8, 2, True), comment='Mức độ loại kết cấu tài khoản')
    active_flag = Column('acc_structure_type_active_flag', NUMBER(1, 2, True), comment='Cờ loại kết cấu tài khoản')


class AccountClassCustomerCategory(Base):
    __tablename__ = 'crm_acc_class_cust_category'
    __table_args__ = {'comment': 'Loại tài khoản Khách hàng'}
    account_class_id = Column(
        'acc_class_id', ForeignKey('crm_acc_class.acc_class_id'), primary_key=True, comment='Mã loại hình khoản'
    )
    customer_category_id = Column(
        'cust_category_id', ForeignKey('crm_cust_category.cust_category_id'),
        primary_key=True, comment='Mã Loại khách hàng'
    )

    account_class = relationship('AccountClass')
    customer_category = relationship('CustomerCategory')


class AccountClassType(Base):
    __tablename__ = 'crm_acc_class_type'
    account_class_id = Column(
        'acc_class_id', ForeignKey('crm_acc_class.acc_class_id'), primary_key=True, comment='Mã loại hình khoản'
    )
    account_type_id = Column('acc_type_id', ForeignKey('crm_acc_type.acc_type_id'))

    account_class = relationship('AccountClass')
    account_type = relationship('AccountType')


class AccountClassCurrency(Base):
    __tablename__ = 'crm_acc_class_currency'
    account_class_id = Column(
        'acc_class_id', ForeignKey('crm_acc_class.acc_class_id'), primary_key=True, comment='Mã loại hình khoản'
    )
    currency_id = Column('currency_id', ForeignKey('crm_currency.currency_id'))

    account_class = relationship('AccountClass')
    currency = relationship('Currency')


class AccountType(Base):
    __tablename__ = 'crm_acc_type'
    __table_args__ = {'comment': 'Loại nhóm sản phẩm (gói) tài khoản'}

    id = Column('acc_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã Loại nhóm sản phẩm (gói) tài khoản')
    code = Column('acc_type_code', VARCHAR(50), comment='Mã code Loại nhóm sản phẩm (gói) tài khoản')
    name = Column('acc_type_name', VARCHAR(255), comment='Tên Loại nhóm sản phẩm (gói) tài khoản')
