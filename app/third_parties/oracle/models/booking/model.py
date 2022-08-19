from sqlalchemy import DATETIME, VARCHAR, Column, ForeignKey, text
from sqlalchemy.dialects.oracle import DATE, NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.form.model import Booking  # noqa
from app.third_parties.oracle.models.master_data.identity import \
    ImageType  # noqa


class BookingAuthentication(Base):
    __tablename__ = 'crm_booking_authentication'

    id = Column('booking_authentication_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động Thông tin xác thực')
    file_uuid = Column(VARCHAR(36), comment='uuid Service File')
    file_uuid_ekyc = Column(VARCHAR(36), comment='uuid Service EKYC')
    created_at = Column(DATETIME, comment='Thời gian tạo')
    image_type_id = Column(ForeignKey('crm_image_type.image_type_id'), nullable=False, comment='Mã loại hình ảnh định danh')
    booking_id = Column(ForeignKey('crm_booking.booking_id'), nullable=False, comment='Mã Giao dịch')

    booking = relationship('Booking')
    image_type = relationship('ImageType')


class BookingCompareImage(Base):
    __tablename__ = 'crm_booking_compare_image'

    id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='(PK) Id Thông tin hình ảnh đối chiếu')
    image_type_id = Column(ForeignKey('crm_image_type.image_type_id'), nullable=False,
                           comment='Mã loại hình ảnh định danh')
    image_uuid = Column(VARCHAR(36), comment='uuid service file ảnh')
    image_ekyc_uuid = Column(VARCHAR(36), comment='uuid ekyc file ảnh')
    is_image_original = Column(NUMBER(1), comment='Cờ đánh dấu hình ảnh dành cho khách hàng')
    compare_image_uuid = Column(VARCHAR(36), comment='uuid service file ảnh đối chiếu')
    compare_image_ekyc_uuid = Column(VARCHAR(36), comment='uuid ekyc file ảnh đối chiếu')
    compare_percent = Column(NUMBER(5, 2), comment='Phần trăm đối chiếu')
    booking_id = Column(VARCHAR(36), comment='ID booking')
    created_at = Column(DATE)

    image_type = relationship('ImageType')
