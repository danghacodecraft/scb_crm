from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Table, text
from sqlalchemy.dialects.oracle import NCLOB, NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base, metadata
from app.third_parties.oracle.models.master_data.others import (  # noqa
    BusinessForm, BusinessType, Sla, TransactionStageLane,
    TransactionStagePhase, TransactionStageStatus
)


class SlaTransaction(Base):
    __tablename__ = 'crm_sla_transaction'
    __table_args__ = {'comment': 'giao dịch SLA'}

    id = Column('sla_transaction_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã giao dịch SLA')
    parent_id = Column('sla_parent_transaction_id', VARCHAR(36), comment='Mã id cha')
    sla_id = Column(ForeignKey('crm_sla.sla_id'), comment='Mã SLA')
    sla_name = Column(VARCHAR(50), comment='Tên giao dịch SLA')
    sla_deadline = Column(NUMBER(10, 0, False), comment='dealine')
    active_flag = Column(NUMBER(1, 0, False), comment='trạng thái')
    created_at = Column(DateTime, comment='ngày tạo')

    sla = relationship('Sla')


class TransactionStage(Base):
    __tablename__ = 'crm_transaction_stage'
    __table_args__ = {'comment': 'Giai đoạn giao dịch'}

    id = Column('transaction_stage_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã bước  giao dịch')
    status_id = Column('transaction_stage_status_id',
                       ForeignKey('crm_transaction_stage_status.transaction_stage_status_id'),
                       comment='Mã trạng thái của  giao dịch')
    lane_id = Column('transaction_stage_lane_id', ForeignKey('crm_transaction_stage_lane.transaction_stage_lane_id'),
                     comment='Mã thông tin đơn vị và phòng ban thực hiện')
    phase_id = Column('transaction_stage_phase_id',
                      ForeignKey('crm_transaction_stage_phase.transaction_stage_phase_id'),
                      comment='Mã giai đoạn')
    business_type_id = Column(ForeignKey('crm_business_type.business_type_id'), comment='Tên bước hiện')
    sla_transaction_id = Column(VARCHAR(36), comment='Mã bước thực hiện kiểu chữ(vd: IN, DUYET)')
    transaction_stage_phase_code = Column(VARCHAR(10), comment='Mã bước thực hiện kiểu chữ(vd: IN, DUYET)')
    transaction_stage_phase_name = Column(VARCHAR(200), comment='Tên bước hiện')
    responsible_flag = Column(NUMBER(1, 0, False), comment='Cờ người chịu trách nhiệm của bước thực hiện')

    business_type = relationship('BusinessType')
    lane = relationship('TransactionStageLane')
    phase = relationship('TransactionStagePhase')
    status = relationship('TransactionStageStatus')


t_crm_stage_lane = Table(
    'crm_stage_lane', metadata,
    Column('lane_id', ForeignKey('crm_lane.lane_id'), comment='Mã luồng xử lý của bước thực hiện'),
    Column('stage_id', ForeignKey('crm_stage.stage_id'), comment='Mã bước  thực hiện'),
    Column('department_id', VARCHAR(36), nullable=False, comment='ID Phòng ban'),
    Column('branch_id', VARCHAR(20), nullable=False, comment='ID Chi nhánh'),
    comment='''Luồng xử lý

  1. Phòng A
  2. Phòng B
  3. Khối A
  '''
)

t_crm_stage_phase = Table(
    'crm_stage_phase', metadata,
    Column('phase_id', ForeignKey('crm_phase.phase_id'), comment='Mã Giai đoạn xử lý'),
    Column('stage_id', ForeignKey('crm_stage.stage_id'), comment='Mã bước thực hiện'),
    comment='''Giai đoạn xử lý

  1. Mở cif
  2. Upload giấy tờ
  3. Ebank
  '''
)


class TransactionDaily(Base):
    __tablename__ = 'crm_transaction_daily'
    __table_args__ = {'comment': 'Giao dịch lưu hằng ngày'}

    transaction_id = Column(VARCHAR(36), primary_key=True, comment='ID chính')
    transaction_state_id = Column(ForeignKey('crm_transaction_stage.transaction_stage_id'),
                                  comment='ID giao đoạn giao dịch')
    transaction_parent_id = Column(ForeignKey('crm_transaction_daily.transaction_id'), comment='ID parent')
    transaction_root_id = Column(VARCHAR(36), comment='Mã root')
    data = Column(NCLOB, comment='Dữ liệu')
    description = Column(VARCHAR(256), comment='Mô tả')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')

    transaction_parent = relationship('TransactionDaily', remote_side=[transaction_id])
    transaction_stage = relationship('TransactionStage')


class TransactionJob(Base):
    __tablename__ = 'crm_transaction_job'

    transaction_id = Column(VARCHAR(36), primary_key=True)
    booking_id = Column(VARCHAR(36), nullable=False)
    business_job_id = Column(VARCHAR(36), nullable=False)
    complete_flag = Column(NUMBER(1, 0, False), nullable=False)
    error_code = Column(VARCHAR(20), nullable=False)
    error_desc = Column(VARCHAR(500), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class Booking(Base):
    __tablename__ = 'crm_booking'
    __table_args__ = {'comment': 'Lưu dữ liệu đẩy qua core'}

    id = Column('booking_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    code = Column('booking_code', VARCHAR(50), comment='Mã code')
    transaction_id = Column(ForeignKey('crm_transaction_daily.transaction_id'), comment='ID Transaction')
    business_type_id = Column('business_type_id', ForeignKey('crm_business_type.business_type_id'),
                              comment='ID type')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')

    business_type = relationship('BusinessType')
    transaction = relationship('TransactionDaily')


class BookingBusinessForm(Base):
    __tablename__ = 'crm_booking_business_form'

    booking_id = Column(ForeignKey('crm_booking.booking_id'), primary_key=True, nullable=False,
                        server_default=text("sys_guid() "))
    business_form_id = Column(ForeignKey('crm_business_form.business_form_id'), primary_key=True, nullable=False)
    save_flag = Column(NUMBER(1, 0, False), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    booking = relationship('Booking')
    business_form = relationship('BusinessForm')


class TransactionAll(Base):
    __tablename__ = 'crm_transaction_all'
    __table_args__ = {'comment': 'Lưu tất cả quan hệ thông tin liên quan giao dịch'}

    transaction_id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "), comment='ID chính')
    transaction_state_id = Column(ForeignKey('crm_transaction_stage.transaction_stage_id'), comment='ID State')
    transaction_parent_id = Column(ForeignKey('crm_transaction_all.transaction_id'))
    transaction_root_id = Column(VARCHAR(36), comment='ID root')
    data = Column(NCLOB, comment='Dữ liệu')
    description = Column(VARCHAR(256), comment='Mô tả')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày chỉnh sửa')
    booking_id = Column(ForeignKey('crm_booking.booking_id'))

    booking = relationship('Booking')
    transaction_parent = relationship('TransactionAll', remote_side=[transaction_id])
    transaction_stage = relationship('TransactionStage')


class TransactionReceiver(Base):
    __tablename__ = 'crm_transaction_recevier'
    __table_args__ = {'comment': 'Các giao dịch tạo cif'}

    transaction_id = Column(ForeignKey('crm_transaction_all.transaction_id'),
                            ForeignKey('crm_transaction_daily.transaction_id'), primary_key=True,
                            comment='Mã giao dịch')
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

    transaction = relationship('TransactionDaily', uselist=False)


class TransactionSender(Base):
    __tablename__ = 'crm_transaction_sender'
    __table_args__ = {'comment': 'Phiên giao dịch tạo cif'}

    transaction_id = Column(ForeignKey('crm_transaction_daily.transaction_id'),
                            ForeignKey('crm_transaction_all.transaction_id'), primary_key=True, comment='Mã giao dịch')
    user_id = Column(VARCHAR(36), comment='Mã user_id')
    user_name = Column(VARCHAR(100), comment='Tên user_id')
    user_fullname = Column(VARCHAR(100), comment='Tên đầy đủ user_id')
    user_email = Column(VARCHAR(100), comment='Email user')
    branch_id = Column(VARCHAR(36), comment='Mã đơn vị')
    branch_code = Column(VARCHAR(10), comment='Mã code đơn vị')
    branch_name = Column(VARCHAR(10), comment='Tên đơn vị')
    department_id = Column(VARCHAR(36), comment='Mã phòng ban thực hiện')
    department_code = Column(VARCHAR(100), comment='Mã code phòng')
    department_name = Column(VARCHAR(100), comment='Tên phòng')
    position_id = Column(VARCHAR(36), comment='Mã khối')
    position_code = Column(VARCHAR(10), comment='Mã code khối')
    position_name = Column(VARCHAR(100), comment='Tên khối')

    transaction = relationship('TransactionDaily', uselist=False)


class BookingAccount(Base):
    __tablename__ = 'crm_booking_account'
    __table_args__ = {'comment': 'Tài khoản booking'}

    booking_id = Column(ForeignKey('crm_booking.booking_id'))
    account_id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))

    booking = relationship('Booking')


class BookingCustomer(Base):
    __tablename__ = 'crm_booking_customer'
    __table_args__ = {'comment': 'Thông tin booking khách hàng'}

    id = Column('booking_customer_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    customer_id = Column(VARCHAR(50))
    booking_id = Column(ForeignKey('crm_booking.booking_id'))

    booking = relationship('Booking')
