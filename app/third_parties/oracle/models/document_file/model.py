from sqlalchemy import DATE, VARCHAR, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.testing.schema import Column

from app.third_parties.oracle.base import Base


class DocumentFileFolder(Base):
    __tablename__ = 'crm_document_file_folder'
    __table_args__ = {'comment': 'Thư mục tệp tài liệu'}

    id = Column('document_file_folder_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    code = Column('document_file_folder_code', VARCHAR(50), nullable=False, comment='Mã thư mục file')
    name = Column('document_file_folder_name', VARCHAR(250), nullable=False, comment='Tên thư mục file')
    level = Column('document_file_folder_level', VARCHAR(250), nullable=False, comment='Cấp độ thư mục')
    parent_id = Column('document_file_folder_parent_id', VARCHAR(50), nullable=False, comment='Mã thư mục cấp cha')


class DocumentFileType(Base):
    __tablename__ = 'crm_document_file_type'
    __table_args__ = {'comment': 'Loại tệp tài liệu'}

    id = Column('document_file_type_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    code = Column('document_file_type_code', VARCHAR(50), nullable=False, comment='Mã loại file')
    name = Column('document_file_type_name', VARCHAR(250), nullable=False, comment='Tên loại file')


class DocumentFile(Base):
    __tablename__ = 'crm_document_file'
    __table_args__ = {'comment': 'Tập tin tài liệu'}

    id = Column('document_file_id', VARCHAR(36), primary_key=True,
                server_default=text("sys_guid() "))
    booking_id = Column(ForeignKey('crm_booking.booking_id'))
    document_file_type_id = Column(ForeignKey('crm_document_file_type.document_file_type_id'))
    document_file_folder_id = Column(ForeignKey('crm_document_file_folder.document_file_folder_id'))
    file_number = Column(VARCHAR(255), nullable=True, comment='Số văn bản')
    parent_id = Column('document_file_parent_id', VARCHAR(36), nullable=True, comment='Mã thư mục cấp cha')
    root_id = Column('document_file_root_id', VARCHAR(36), nullable=True, comment='Mã thư mục gốc')
    file_uuid = Column(VARCHAR(255), nullable=True, comment='UUID của file')
    expired_date = Column(DATE, nullable=True, comment='Ngày hết hiệu lực')
    created_by_branch_name = Column(VARCHAR(255), nullable=True, comment='Tên nơi khởi tạo')
    created_by_branch_code = Column(VARCHAR(255), nullable=True, comment='Mã nơi khởi tạo')
    created_by_user_name = Column(VARCHAR(255), nullable=True, comment='Tên người khởi tạo')
    created_by_user_code = Column(VARCHAR(255), nullable=True, comment='Mã người khởi tạo')
    updated_by_user_name = Column(VARCHAR(255), nullable=True, comment='Tên người cập nhập')
    updated_by_user_code = Column(VARCHAR(255), nullable=True, comment='Mã người cập nhập')

    booking = relationship('Booking')
    document_file_type = relationship('DocumentFileType')
    document_file_folder = relationship('DocumentFileFolder')
