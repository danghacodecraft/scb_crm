from sqlalchemy import DATETIME, VARCHAR, Column, ForeignKey, text
from sqlalchemy.dialects.oracle import DATE, NUMBER
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.model import \
    Customer  # noqa
from app.third_parties.oracle.models.cif.form.model import Booking  # noqa


class BookingAuthentication(Base):
    __tablename__ = 'crm_booking_authentication'

    id = Column('booking_authentication_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "),
                comment='Mã gen tự động Thông tin xác thực')
    teller_username = Column(VARCHAR(100), comment='Tên đăng nhập của teller kết nối với tablet', nullable=False)
    identity_number = Column(VARCHAR(30), comment='Số giấy tờ định danh')
    identity_front_document_file_uuid = Column(VARCHAR(36), comment='uuid Service File')
    identity_front_document_file_uuid_ekyc = Column(VARCHAR(36), comment='uuid Service EKYC')
    face_file_uuid = Column(VARCHAR(36), comment='uuid Service File')
    face_file_uuid_ekyc = Column(VARCHAR(36), comment='uuid Service EKYC')
    created_at = Column(DATETIME, comment='Thời gian tạo')
    image_type_id = Column(ForeignKey('crm_image_type.image_type_id'), nullable=False, comment='Mã loại hình ảnh định danh')
    booking_id = Column(ForeignKey('crm_booking.booking_id'), nullable=False, comment='Mã Giao dịch')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), comment='ID khách hàng (nếu có)')

    booking = relationship('Booking')
    customer = relationship('Customer')


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
