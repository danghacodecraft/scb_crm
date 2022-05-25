from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, text
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

    id = Column('comment_id', VARCHAR(36), primary_key=True, server_default=text("sys_guid() "))
    booking_id = Column(ForeignKey('crm_booking.booking_id'))

    username = Column('user_username', VARCHAR(255), nullable=False,
                      comment='Username người tạo comment')
    name = Column('name', VARCHAR(255), nullable=False,
                  comment='Tên người tạo comment')
    code = Column('code', VARCHAR(36), nullable=False,
                  comment='Mã nhân viên người tạo comment')
    email = Column('email', VARCHAR(255), nullable=False,
                   comment='Email người tạo comment')
    hrm_department_id = Column('hrm_department_id', VARCHAR(36), nullable=True,
                               comment='ID Phòng ban người tạo comment')
    hrm_department_code = Column('hrm_department_code', VARCHAR(10), nullable=True,
                                 comment='Mã Phòng ban người tạo comment')
    hrm_department_name = Column('hrm_department_name', VARCHAR(100), nullable=True,
                                 comment='Tên Phòng ban người tạo comment')
    hrm_branch_id = Column('hrm_branch_id', VARCHAR(36), nullable=True,
                           comment='ID Chi nhánh/Hội sở người tạo comment')
    hrm_branch_code = Column('hrm_branch_code', VARCHAR(10), nullable=True,
                             comment='Mã Chi nhánh/Hội sở người tạo comment')
    hrm_branch_name = Column('hrm_branch_name', VARCHAR(100), nullable=True,
                             comment='Tên Chi nhánh/Hội sở người tạo comment')
    hrm_title_id = Column('hrm_title_id', VARCHAR(36), nullable=False,
                          comment='ID Chức danh người tạo comment')
    hrm_title_code = Column('hrm_title_code', VARCHAR(10), nullable=False,
                            comment='Mã Chức danh người tạo comment')
    hrm_title_name = Column('hrm_title_name', VARCHAR(100), nullable=False,
                            comment='Tên Chức danh người tạo comment')
    hrm_position_id = Column('hrm_position_id', VARCHAR(36), nullable=True,
                             comment='ID Chức vụ người tạo comment')
    hrm_position_code = Column('hrm_position_code', VARCHAR(10), nullable=True,
                               comment='Mã chức vụ người tạo comment')
    hrm_position_name = Column('hrm_position_name', VARCHAR(100), nullable=True,
                               comment='Tên chức vụ người tạo comment')
    content = Column('content', VARCHAR(500), nullable=False, comment='Nội dung bình luận')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    updated_at = Column('updated_at', DateTime, nullable=True, comment='Ngày cập nhật')
    url = Column('url', VARCHAR(200), nullable=True, comment='URL file đính kèm')

    booking = relationship('Booking')
