from sqlalchemy import DATETIME, VARCHAR, Column, ForeignKey, text
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
