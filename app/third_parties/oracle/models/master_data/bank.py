from sqlalchemy import VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class BankBranch(Base):
    __tablename__ = 'crm_bank_branch'

    id = Column('bank_branch_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chi nhánh ngân hàng')
    code = Column('bank_branch_code', VARCHAR(50), nullable=False, comment='Mã chi nhánh ngân hàng')
    name = Column('bank_branch_name', VARCHAR(255), nullable=False, comment='Tên chi nhánh ngân hàng')
    bank_id = Column('bank_id', VARCHAR(36), nullable=False, comment='Mã ngân hàng')
    bank_account_number = Column('bank_account_num', VARCHAR(15), nullable=False, comment='Số tài khoản nhánh ngân hàng')


class Bank(Base):
    __tablename__ = 'crm_bank'

    id = Column('bank_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID ngân hàng')
    code = Column('bank_code', VARCHAR(50), nullable=False, comment='Mã ngân hàng')
    name = Column('bank_name', VARCHAR(255), nullable=False, comment='Tên ngân hàng')
    napas_flag = Column(NUMBER(1), nullable=False, comment='Napas')
    citad_flag = Column(NUMBER(1), nullable=False, comment='Citad')
