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

    username = Column('created_user_username', VARCHAR(100), nullable=False,
                      comment='Tên nick name tạo comment')
    created_at = Column('created_at', DateTime, nullable=False, comment='Ngày tạo')
    content = Column(VARCHAR(36), comment='Nội dung bình luận')
    url = Column(VARCHAR(200), comment='URL file đính kèm')
