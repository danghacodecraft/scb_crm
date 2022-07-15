from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.oracle import BLOB, CLOB, NCLOB, NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.master_data.others import (  # noqa
    BusinessForm, BusinessType
)
from app.utils.functions import orjson_dumps


class TransactionDaily(Base):
    __tablename__ = 'crm_transaction_daily'
    __table_args__ = {'comment': 'Giao dịch lưu hằng ngày'}

    transaction_id = Column(VARCHAR(36), primary_key=True, comment='ID chính')
    transaction_stage_id = Column(ForeignKey('crm_transaction_stage.transaction_stage_id'),
                                  comment='ID giao đoạn giao dịch')
    transaction_parent_id = Column(ForeignKey('crm_transaction_daily.transaction_id'), comment='ID parent')
    transaction_root_id = Column(VARCHAR(36), comment='Mã root')
    data = Column(NCLOB, comment='Dữ liệu')
    description = Column(VARCHAR(256), comment='Mô tả')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')

    is_reject = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                       comment='Cờ đánh dấu trạng thái TRẢ hồ sơ')
    is_cancel = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                       comment='Cờ đánh dấu trạng thái HỦY hồ sơ')

    transaction_parent = relationship('TransactionDaily', remote_side=[transaction_id])
    transaction_stage = relationship('TransactionStage')


class TransactionAll(Base):
    __tablename__ = 'crm_transaction_all'
    __table_args__ = {'comment': 'Lưu tất cả quan hệ thông tin liên quan giao dịch'}

    transaction_id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    transaction_stage_id = Column(ForeignKey('crm_transaction_stage.transaction_stage_id'), comment='ID State')
    transaction_parent_id = Column(ForeignKey('crm_transaction_all.transaction_id'))
    transaction_root_id = Column(VARCHAR(36), comment='ID root')
    data = Column(NCLOB, comment='Dữ liệu')
    description = Column(VARCHAR(256), comment='Mô tả')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')

    is_reject = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                       comment='Cờ đánh dấu trạng thái TRẢ hồ sơ')
    is_cancel = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "),
                       comment='Cờ đánh dấu trạng thái HỦY hồ sơ')

    transaction_parent = relationship('TransactionAll', remote_side=[transaction_id])
    transaction_stage = relationship('TransactionStage')


class TransactionReceiver(Base):
    __tablename__ = 'crm_transaction_recevier'
    __table_args__ = {'comment': 'Các giao dịch tạo cif'}

    # transaction_id = Column(ForeignKey('crm_transaction_all.transaction_id'),
    #                         ForeignKey('crm_transaction_daily.transaction_id'), primary_key=True,
    #                         comment='Mã giao dịch')
    transaction_id = Column(VARCHAR(36), primary_key=True, comment='Mã transaction_id')
    user_id = Column(VARCHAR(36), comment='Mã user_id')
    user_name = Column(VARCHAR(100), comment='Tên user_id')
    user_fullname = Column(VARCHAR(100), comment='Tên đầy đủ user_id')
    user_email = Column(VARCHAR(100), comment='Email')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị')
    branch_code = Column(VARCHAR(10), comment='Mã code đơn vị')
    branch_name = Column(VARCHAR(100), comment='Tên đơn vị')
    department_id = Column(VARCHAR(36), comment='Mã phòng ban thực hiện')
    department_code = Column(VARCHAR(10), comment='Mã code phòng')
    department_name = Column(VARCHAR(100), comment='Tên phòng')
    position_id = Column(VARCHAR(36), comment='Mã khối')
    position_code = Column(VARCHAR(10), comment='Mã code khối')
    position_name = Column(VARCHAR(100), comment='Tên khối')
    title_id = Column(VARCHAR(36), comment='Mã chức danh')
    title_code = Column(VARCHAR(10), comment='Mã code chức danh')
    title_name = Column(VARCHAR(100), comment='Tên chức danh')

    # transaction = relationship('TransactionDaily', uselist=False)


class TransactionSender(Base):
    __tablename__ = 'crm_transaction_sender'
    __table_args__ = {'comment': 'Phiên giao dịch tạo cif'}

    # transaction_id = Column(ForeignKey('crm_transaction_daily.transaction_id'),
    #                         ForeignKey('crm_transaction_all.transaction_id'), primary_key=True, comment='Mã giao dịch')
    transaction_id = Column(VARCHAR(36), primary_key=True, comment='Mã transaction_id')
    user_id = Column(VARCHAR(36), comment='Mã user_id')
    user_name = Column(VARCHAR(100), comment='Tên user_id')
    user_fullname = Column(VARCHAR(100), comment='Tên đầy đủ user_id')
    user_email = Column(VARCHAR(100), comment='Email user')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị')
    branch_code = Column(VARCHAR(10), comment='Mã code đơn vị')
    branch_name = Column(VARCHAR(100), comment='Tên đơn vị')
    department_id = Column(VARCHAR(36), comment='Mã phòng ban thực hiện')
    department_code = Column(VARCHAR(100), comment='Mã code phòng')
    department_name = Column(VARCHAR(100), comment='Tên phòng')
    position_id = Column(VARCHAR(36), comment='Mã khối')
    position_code = Column(VARCHAR(10), comment='Mã code khối')
    position_name = Column(VARCHAR(100), comment='Tên khối')
    title_id = Column(VARCHAR(36), comment='Mã chức danh')
    title_code = Column(VARCHAR(10), comment='Mã code chức danh')
    title_name = Column(VARCHAR(100), comment='Tên chức danh')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column('update_at', DateTime, comment='Ngày chỉnh sửa')

    # transaction = relationship('TransactionDaily', uselist=False)


class Booking(Base):
    __tablename__ = 'crm_booking'
    __table_args__ = {'comment': 'Lưu dữ liệu đẩy qua core'}

    id = Column('booking_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    code = Column('booking_code', VARCHAR(50), comment='Mã code')
    transaction_id = Column(ForeignKey('crm_transaction_daily.transaction_id'), comment='ID Transaction')
    parent_id = Column('booking_parent_id', ForeignKey('crm_booking.booking_id'), comment='ID Booking cha')
    business_type_id = Column('business_type_id', ForeignKey('crm_business_type.business_type_id'),
                              comment='ID type')

    branch_id = Column(VARCHAR(50), comment='Mã đơn vị')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')
    created_by = Column(DateTime, comment='Người tạo')
    updated_by = Column(DateTime, comment='Người chỉnh sửa')

    business_type = relationship('BusinessType')
    transaction = relationship('TransactionDaily')


class BookingAccount(Base):
    __tablename__ = 'crm_booking_account'
    __table_args__ = {'comment': 'Tài khoản booking'}
    id = Column('booking_account_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    booking_id = Column('booking_id')
    customer_id = Column(VARCHAR(36), comment="Mã KH")
    account_id = Column('casa_account_id', VARCHAR(36))
    td_account_id = Column('td_account_id', VARCHAR(36), comment="ID Tài khoản tiết kiệm (TD)")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class BookingCustomer(Base):
    __tablename__ = 'crm_booking_customer'
    __table_args__ = {'comment': 'Thông tin booking khách hàng'}

    id = Column('booking_customer_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    customer_id = Column(VARCHAR(50))
    booking_id = Column(ForeignKey('crm_booking.booking_id'))

    booking = relationship('Booking')


class BookingBusinessForm(Base):
    __tablename__ = 'crm_booking_business_form'

    booking_id = Column(ForeignKey('crm_booking.booking_id'), primary_key=True, nullable=False,
                        server_default=text("sys_guid() "))
    business_form_id = Column(ForeignKey('crm_business_form.business_form_id'), primary_key=True, nullable=False)
    save_flag = Column(NUMBER(1, 0, False), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    form_data = Column(BLOB, comment='Dữ liệu template nhập', default=orjson_dumps([]))
    log_data = Column(BLOB, comment='Data lưu Lịch sử hồ sơ', default=orjson_dumps([]))
    out_data = Column(CLOB, comment='Data GW trả về', default=orjson_dumps([]))
    booking = relationship('Booking')
    business_form = relationship('BusinessForm')
