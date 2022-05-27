from sqlalchemy import BLOB, VARCHAR, Column, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from app.third_parties.oracle.base import Base
from app.third_parties.oracle.models.cif.basic_information.model import (  # noqa
    Customer
)
from app.third_parties.oracle.models.master_data.others import (  # noqa
    HrmEmployee
)


class CustomerEmployee(Base):
    __tablename__ = 'crm_cust_employee'
    __table_args__ = {'comment': 'Nhân viên - khách hàng'}

    id = Column('cust_employee_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    staff_type_id = Column(ForeignKey('crm_staff_type.staff_type_id'), comment='Mã Danh mục Loại nhân viên giới thiệu')
    employee_id = Column(ForeignKey('hrm_employee.id'), nullable=False, comment='Mã nhân viên')
    customer_id = Column(ForeignKey('crm_customer.customer_id'), nullable=False, comment='Mã khách hàng')
    created_at = Column(DateTime, comment='Ngày tạo')
    updated_at = Column(DateTime, comment='Ngày cập nhật')

    customer = relationship('Customer')
    employee = relationship('HrmEmployee')


class Comment(Base):
    __tablename__ = 'crm_comment'
    __table_args__ = {'comment': 'Bình luận'}

    id = Column(VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    booking_id = Column(ForeignKey('crm_booking.booking_id'))

    username = Column(VARCHAR(255), nullable=False,
                      comment='Username người tạo comment')
    name = Column(VARCHAR(255), nullable=False,
                  comment='Tên người tạo comment')
    code = Column(VARCHAR(36), nullable=False,
                  comment='Mã nhân viên người tạo comment')
    email = Column(VARCHAR(255), nullable=False,
                   comment='Email người tạo comment')
    avatar_url = Column(VARCHAR(250), nullable=False,
                        comment='URL ảnh đại diện')
    hrm_department_id = Column(VARCHAR(36), nullable=True,
                               comment='ID Phòng ban người tạo comment')
    hrm_department_code = Column(VARCHAR(10), nullable=True,
                                 comment='Mã Phòng ban người tạo comment')
    hrm_department_name = Column(VARCHAR(100), nullable=True,
                                 comment='Tên Phòng ban người tạo comment')
    hrm_branch_id = Column(VARCHAR(36), nullable=True,
                           comment='ID Chi nhánh/Hội sở người tạo comment')
    hrm_branch_code = Column(VARCHAR(10), nullable=True,
                             comment='Mã Chi nhánh/Hội sở người tạo comment')
    hrm_branch_name = Column(VARCHAR(100), nullable=True,
                             comment='Tên Chi nhánh/Hội sở người tạo comment')
    hrm_title_id = Column(VARCHAR(36), nullable=False,
                          comment='ID Chức danh người tạo comment')
    hrm_title_code = Column(VARCHAR(10), nullable=False,
                            comment='Mã Chức danh người tạo comment')
    hrm_title_name = Column(VARCHAR(100), nullable=False,
                            comment='Tên Chức danh người tạo comment')
    hrm_position_id = Column(VARCHAR(36), nullable=True,
                             comment='ID Chức vụ người tạo comment')
    hrm_position_code = Column(VARCHAR(10), nullable=True,
                               comment='Mã chức vụ người tạo comment')
    hrm_position_name = Column(VARCHAR(100), nullable=True,
                               comment='Tên chức vụ người tạo comment')
    content = Column(VARCHAR(500), nullable=False, comment='Nội dung bình luận')
    created_at = Column(DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column(DateTime, nullable=True, comment='Ngày cập nhật')
    file_uuid = Column(BLOB, nullable=False, comment='URL file đính kèm')

    booking = relationship('Booking')
