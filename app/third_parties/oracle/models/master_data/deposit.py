from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class TDRolloverType(Base):
    __tablename__ = 'crm_td_rollover_type'
    __table_args__ = {'comment': 'Chỉ định khi đến hạn (Loại tái ký)'}

    id = Column('td_rollover_type_id', VARCHAR(36), primary_key=True, comment='ID chính')
    code = Column('td_rollover_type_code', VARCHAR(10), nullable=False, comment='Mã code')
    name = Column('td_rollover_type_name', VARCHAR(100), nullable=False, comment='Tên')
    active_flag = Column('active_flag', NUMBER(1, 0, False), comment='Trạng thái')


class TDAccClass(Base):
    __tablename__ = 'crm_td_acc_class'
    __table_args__ = {'comment': ''}

    id = Column('td_acc_class_id', VARCHAR(10), primary_key=True, comment='ID chính')
    code = Column('td_acc_class_code', VARCHAR(10), nullable=False, comment='Mã code')
    name = Column('td_acc_class_name', VARCHAR(100), nullable=False, comment='Tên')
    gl_fcc_so_du_tg = Column('gl_fcc_so_du_tg', VARCHAR(16), nullable=False, comment='Tài khoản treo số dư tiền gửi')
    active_flag = Column('active_flag', NUMBER(1, 0, False), comment='Trạng thái')


# class TDAccClassCategory(Base):
#     __tablename__ = 'crm_td_acc_class_cust_category'
#     __table_args__ = {'comment': 'Loại tài khoản TD và tái ký'}
#
#     td_acc_class_id = Column(ForeignKey('crm_td_acc_class.td_acc_class_id'), comment='ID Sản phẩm tiền gửi')
#     cust_category_id = Column(ForeignKey('crm_cust_category.cust_category_id'), comment='ID Đối tượng khách hàng ')

#
# class TDAccClassRolloverType(Base):
#     __tablename__ = 'crm_td_acc_class_rollover_type'
#     __table_args__ = {'comment': ''}
#
#     td_acc_class_id = Column(ForeignKey('crm_td_acc_class.td_acc_class_id'), comment='ID Sản phẩm tiền gửi')
#     td_rollover_id = Column(ForeignKey('crm_td_rollover_type.td_rollover_id'), comment='ID Loại tái ký')
