
from sqlalchemy import DATETIME, VARCHAR, Column, text
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class Tablet(Base):
    __tablename__ = 'crm_tablet'

    id = Column('tablet_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    teller_username = Column(VARCHAR(100), comment='Tên đăng nhập của teller kết nối với tablet', nullable=False)
    otp = Column(VARCHAR(6), comment='Mã OTP để kết nối web với tablet', nullable=False)
    created_at = Column(DATETIME, comment='Thời gian tạo OTP')
    expired_at = Column(DATETIME, comment='Thời gian hết hạn OTP')
    device_information = Column(VARCHAR(500), comment='Thông tin tablet')
    is_paired = Column(NUMBER(1), comment='Nhận biết web và tablet đã kết nối với nhau hay chưa', default=0)
